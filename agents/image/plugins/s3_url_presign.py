from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from typing import Optional, Dict, Tuple
from google.adk.models import LlmRequest, LlmResponse
from src.bucket.manager import S3BucketManager
import logging
from google.genai.types import FileData

logger = logging.getLogger(__name__)


class S3UrlPresignPlugin(BasePlugin):
        
    def __init__(self, name: str = "s3_url_presign_plugin"):
        super().__init__(name)
        self.s3_manager = S3BucketManager()
        # presigned_url -> original_s3_uri 매핑을 저장
        self._url_mapping: Dict[str, Tuple[str, str, str]] = {}  # {presigned_url: (s3_uri, mime_type, display_name)}
    
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
                    
                    # 원본 정보 저장 (presigned URL -> 원본 S3 URI)
                    self._url_mapping[presigned_url] = (file_uri, mime_type, display_name)
                    
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
    
    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> Optional[LlmResponse]:
        """
        LLM 응답의 parts 내에 presigned URL이 있는 경우 원본 S3 URI로 복원
        """
        try:
            # content가 없거나 parts가 없으면 early return
            if not llm_response.content or not llm_response.content.parts:
                return None
            
            # parts를 enumerate로 순회
            for idx, part in enumerate(llm_response.content.parts):
                # file_data가 없으면 skip
                if not (hasattr(part, 'file_data') and part.file_data):
                    continue
                
                file_uri = getattr(part.file_data, 'file_uri', None)
                
                # 매핑에 있는 presigned URL이면 원본 S3 URI로 복원
                if file_uri and file_uri in self._url_mapping:
                    original_s3_uri, mime_type, display_name = self._url_mapping[file_uri]
                    
                    # 원본 S3 URI로 교체
                    llm_response.content.parts[idx].file_data = FileData(
                        file_uri=original_s3_uri,
                        mime_type=mime_type,
                        display_name=display_name
                    )
                    
                    # 매핑에서 제거 (메모리 정리)
                    del self._url_mapping[file_uri]
                    
                    logger.info(f"[S3UrlPresignPlugin] Restored S3 URI: {original_s3_uri}")
            
            return None
            
        except Exception as e:
            logger.error(f"[S3UrlPresignPlugin] Error restoring S3 URI: {e}")
            return None