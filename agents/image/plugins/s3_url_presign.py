from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from typing import Optional
from google.adk.models import LlmRequest, LlmResponse
from src.bucket.manager import S3BucketManager
import logging
from google.genai.types import FileData

logger = logging.getLogger(__name__)


class S3UrlPresignPlugin(BasePlugin):
        
    def __init__(self, name: str = "s3_url_presign_plugin"):
        super().__init__(name)
        self.s3_manager = S3BucketManager()
    
    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        """
        LLM 요청의 parts 내에 S3 URI가 있는 경우 presigned URL로 변경
        """
        try:
            # contents가 없으면 early return
            if not llm_request.contents:
                return None
            
            # 모든 Content를 순회
            for content in llm_request.contents:
                # parts가 없으면 skip
                if not content.parts:
                    continue
                
                # parts를 enumerate로 순회
                for idx, part in enumerate(content.parts):
                    # file_data가 없으면 skip
                    if not (hasattr(part, 'file_data') and part.file_data):
                        continue
                    
                    file_uri = getattr(part.file_data, 'file_uri', None)
                    
                    # S3 URI가 아니면 skip
                    if not (file_uri and file_uri.startswith("s3://giga-banana/")):
                        continue
                    
                    presigned_url = self.s3_manager.generate_presigned_url(
                        file_uri=file_uri,
                        expiration=3600  # 1시간
                    )
                    
                    mime_type = part.file_data.mime_type
                    display_name = getattr(part.file_data, 'display_name', None)
                    
                    # 새로운 FileData 객체로 교체
                    content.parts[idx].file_data = FileData(
                        file_uri=presigned_url,
                        mime_type=mime_type,
                        display_name=display_name
                    )
            
            # 수정된 요청이 LLM으로 전달되도록 None 반환
            return None
            
        except Exception as e:
            logger.error(f"[S3UrlPresignPlugin] Error converting S3 URI: {e}")
            # 에러가 발생해도 요청은 계속 진행
            return None