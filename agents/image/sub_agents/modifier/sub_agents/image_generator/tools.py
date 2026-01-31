from __future__ import annotations

import asyncio
import base64
from typing import Any

import requests
from pydantic import BaseModel

from src.bucket.manager import S3BucketManager

# API
API_BASE_URL = "https://ui5lkk116duoen-8188.proxy.runpod.net/api/v2"
WORKFLOW_RUN_URL = f"{API_BASE_URL}/workflow/run?response_format=base64"
TAGGER_IMAGES_URL = f"{API_BASE_URL}/tagger/images"

# Defaults
DEFAULT_TOP_N = 10
MIME_TYPE_JPEG = "image/jpeg"

_bucket_manager: S3BucketManager | None = None


def _get_bucket_manager() -> S3BucketManager:
    """S3BucketManager 싱글톤 (모듈 스코프)."""
    global _bucket_manager
    if _bucket_manager is None:
        _bucket_manager = S3BucketManager()
    return _bucket_manager


def decode_image(base64_image: str) -> bytes:
    return base64.b64decode(base64_image)


def encode_image(file_data: bytes) -> str:
    return base64.b64encode(file_data).decode("utf-8")


def download_image(image_url: str) -> bytes:
    bucket_manager = S3BucketManager()
    s3_url = bucket_manager.generate_presigned_url(image_url)
    response = requests.get(s3_url, timeout=30)
    response.raise_for_status()
    return response.content


class GeneratedImageResponse(BaseModel):
    user_id: str
    image_url: str
    workflow: dict[str, Any] | None = None

    @classmethod
    async def create_from_response(
        cls, 
        response: requests.Response,
        workflow: dict[str, Any] | None = None
    ) -> GeneratedImageResponse:
        response.raise_for_status()
        body = response.json()
        user_id: str = body["user_id"]
        base64_image: str = body["images"][0]
        file_data = decode_image(base64_image)

        bucket_manager = _get_bucket_manager()
        image_url = await bucket_manager.upload_file(
                user_id=user_id,
                file_data=file_data,
                mime_type=MIME_TYPE_JPEG,
        )

        if image_url is None:
            raise RuntimeError("S3 upload returned no URL")
        
        # Creations 테이블에 저장
        from src.database.session import RDS_Session
        from src.session.service import create_creation
        import logging
        
        logger = logging.getLogger(__name__)
        
        db = RDS_Session()
        try:
            create_creation(
                db=db,
                user_id=user_id,
                image_url=image_url,
                workflow=workflow,  # 워크플로우 저장
                creation_metadata=None  # meta_data는 비워둠
            )
            logger.info(f"Creation record saved for modified image: {image_url}")
        except Exception as db_error:
            logger.error(f"Failed to save creation record: {db_error}", exc_info=True)
            # DB 저장 실패해도 image_url은 반환 (이미지는 생성됨)
        finally:
            db.close()
        
        return cls(user_id=user_id, image_url=image_url, workflow=workflow)



async def generate_image(user_id: str, workflow: dict[str, Any]) -> dict[str, str]:
    """
    이미지를 생성합니다.

    Args:
        user_id: 사용자 ID
        workflow: 워크플로우 정의

    Returns:
        dict[str, str]: 이미지 생성 결과 ({"user_id": user_id, "image_url": image_url})
    """
    payload = {"user_id": user_id, "workflow": workflow}
    response = requests.post(WORKFLOW_RUN_URL, json=payload, timeout=120)
    res = await GeneratedImageResponse.create_from_response(response, workflow=workflow)
    return res.model_dump_json()


def extract_image_prompt(image_url: str, top_n: int = DEFAULT_TOP_N) -> list[str]:
    """
    이미지의 프롬프트(태그)를 추출합니다.

    Args:
        image_url: 이미지 URL
        top_n: 반환할 태그 개수 (기본 10)

    Returns:
        태그 문자열 리스트 (예: ["1girl", "solo", "long_hair", ...])
    """
    file_data = download_image(image_url)
    base64_image = encode_image(file_data)
    payload = {"base64_image": base64_image, "top_n": top_n}

    response = requests.post(TAGGER_IMAGES_URL, json=payload, timeout=30)
    response.raise_for_status()
    body = response.json()
    return body["tags"]
