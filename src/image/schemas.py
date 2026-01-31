from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
    

class ImageRequest(BaseModel):
    """이미지 생성 / 수정 요청 모델"""
    user_id: str = Field(None, description="사용자 ID")
    session_id: str = Field(None, description="세션 ID")
    user_message: str = Field(..., description="사용자 메시지", min_length=1)
    context: Optional[Dict[str, Any]] = Field(None, description="추가 컨텍스트")
    image_upload_url: Optional[str] = Field(None, description="S3 파일 URI")
    image_upload_mime_type: Optional[str] = Field(None, description="MIME 타입")