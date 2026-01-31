from pydantic import BaseModel, Field

class ImageUploadRequest(BaseModel):
    """이미지 업로드 요청"""
    user_id: str = Field(..., description="사용자 ID")
    file_name: str | None = Field(None, description="파일명 (선택사항)")

class ImageUploadResponse(BaseModel):
    """이미지 업로드 응답"""
    image_upload_uri: str = Field(..., description="S3 URI")
    message: str = Field(default="이미지가 성공적으로 업로드되었습니다.")