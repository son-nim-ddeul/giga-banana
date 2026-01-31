import base64
import asyncio
from pydantic import BaseModel
import requests

from src.bucket.manager import S3BucketManager


class GeneratedImageResponse(BaseModel):
    user_id: str
    image_url: str

    @classmethod
    def crate_with_decode(cls, response: requests.Response) -> 'GeneratedImageResponse':
        response.raise_for_status()
        body = response.json()
        user_id: str = body["user_id"]
        base64_image: str = body["images"][0]
        file_data = base64.b64decode(base64_image)

        bucket_manager = S3BucketManager()
        image_url = asyncio.run(
            bucket_manager.upload_file(
                user_id=user_id,
                file_data=file_data,
                mime_type="image/jpeg",
            )
        )
        return cls(user_id=user_id, image_url=image_url)


def generate_image(user_id: str, workflow: dict, ) -> GeneratedImageResponse:
    """
    이미지를 생성합니다.

    Args:
        user_id: str: 사용자 ID
        workflow: dict: 워크플로우

    Returns:
        GeneratedImageResponse: 이미지 생성 결과
    """
    url = "https://ui5lkk116duoen-8188.proxy.runpod.net/api/v2/workflow/run"
    request_body = {
        "user_id": user_id,
        "workflow": workflow
    }
    response = requests.post(url, json=request_body)
    return GeneratedImageResponse.crate_with_decode(response)
