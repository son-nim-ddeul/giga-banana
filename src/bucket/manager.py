from __future__ import annotations

import logging
import uuid
from contextlib import asynccontextmanager
from typing import Any, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class S3BucketManager(BaseModel):

    _session: Any = None

    model_config = {
        "arbitrary_types_allowed": True, 
        "validate_assignment": True, 
        "extra": "forbid"
    }

    # s3://giga-banana/images/{user_id}/{uuid}.jpg
    async def _get_session(self):
        import aioboto3
        if self._session is None:
            session_kwargs = {
                "region_name": "ap-northeast-2",
                "bucket_name": "giga-banana"
            }
            
            self._session = aioboto3.Session(**session_kwargs)
        
        return self._session

    @asynccontextmanager
    async def _client(self):
        session = await self._get_session()
        async with session.client(service_name="s3") as s3:
            yield s3


    async def upload_file(
        self,
        user_id: str,
        file_data: bytes,
        mime_type: str,
        file_name: str | None = None,
    ) -> Optional[str]:
        """S3 파일 업로드 및 S3 URI 반환 메서드"""

        async with self._client() as s3:
            if file_name is None:
                file_name = str(uuid.uuid4())
            key = f"images/{user_id}/{file_name}.jpg"
            body = file_data
            try:
                await s3.put_object(
                    Bucket="giga-banana",
                    Key=key,
                    Body=body,
                    ContentType=mime_type
                )

                file_uri = f"s3://giga-banana/{key}"
                return file_uri
            except Exception as e:
                logger.error(f"Failed to upload file: {e}")
                raise e