from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
import logging

from src.bucket.manager import S3BucketManager
from src.bucket.schemas import ImageUploadResponse

logger = logging.getLogger(__name__)

router = APIRouter()

bucket_manager = S3BucketManager()

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    user_id: str = Form(..., description="사용자 ID"),
    file: UploadFile = File(..., description="업로드할 이미지 파일"),
    file_name: Optional[str] = Form(None, description="파일명 (선택사항)")
) -> ImageUploadResponse:
    """
    클라이언트에서 이미지를 S3에 업로드합니다.
    
    - **user_id**: 사용자 ID
    - **file**: 업로드할 이미지 파일 (multipart/form-data)
    - **file_name**: 선택적 파일명 (지정하지 않으면 UUID 사용)
    """
    try:
        # 파일 타입 검증
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, 
                detail=f"이미지 파일만 업로드 가능합니다. 현재 타입: {file.content_type}"
            )
        
        # 파일 데이터 읽기
        file_data = await file.read()
        
        # S3에 업로드
        file_uri = await bucket_manager.upload_file(
            user_id=user_id,
            file_data=file_data,
            mime_type=file.content_type,
            file_name=file_name
        )
        
        if not file_uri:
            raise HTTPException(status_code=500, detail="파일 업로드에 실패했습니다.")
        
        logger.info(f"File uploaded successfully: {file_uri}")
        
        return ImageUploadResponse(
            image_upload_uri=file_uri,
            message="이미지가 성공적으로 업로드되었습니다."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to upload image: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"이미지 업로드 중 오류가 발생했습니다: {str(e)}"
        )