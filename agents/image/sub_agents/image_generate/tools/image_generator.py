import asyncio
import mimetypes
import logging
from datetime import datetime
import uuid
from google.adk.tools.tool_context import ToolContext

from google import genai
from google.genai import types

from src.bucket.manager import S3BucketManager
from src.config import settings

logger = logging.getLogger(__name__)

# 시스템 프롬프트: 이미지 생성 가이드라인
IMAGE_GENERATION_SYSTEM_PROMPT = """
You are an expert AI image generation assistant.
Generate high-quality images based on the provided detailed prompt.
Focus on:
- Visual accuracy and detail
- Proper composition and lighting
- Professional quality output
- Adherence to the prompt specifications
"""


async def _generate_image_async(
    prompt: str,
    user_id: str,
    aspect_ratio: str = "1:1",
    image_size: str = "1K"
) -> str:
    """
    Gemini API를 사용하여 이미지 생성 및 S3 업로드 (내부 async 함수)
    """
    
    if not settings.google_api_key:
        raise Exception("GOOGLE_API_KEY가 설정되지 않았습니다.")
    
    try:
        logger.info(f"이미지 생성 시작 - user_id: {user_id}")
        
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=settings.google_api_key)
        
        # API 요청 콘텐츠 구성
        contents = [
            types.Part.from_text(text=prompt)
        ]
        
        # 생성 설정
        config = types.GenerateContentConfig(
            system_instruction=IMAGE_GENERATION_SYSTEM_PROMPT,
            temperature=1.0,
            candidate_count=1,
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size
            )
        )
        
        # Gemini API 호출
        logger.info("Gemini API 호출 중...")
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=contents,
            config=config
        )
        
        logger.info(f"Gemini 응답 수신")
        
        # 응답 처리
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                logger.info(f"텍스트 응답: {part.text}")
            elif part.inline_data is not None:
                # 이미지 데이터 처리
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type
                file_extension = mimetypes.guess_extension(mime_type) or ".jpg"
                
                # 파일명 생성
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}_{uuid.uuid4()}{file_extension}"
                
                logger.info(f"이미지 생성 완료, S3 업로드 시작 - file_name: {file_name}")
                
                # S3 업로드 (async)
                bucket_manager = S3BucketManager()
                s3_uri = await bucket_manager.upload_file(
                    user_id=user_id,
                    file_data=image_data,
                    mime_type=mime_type,
                    file_name=file_name
                )
                
                logger.info(f"S3 업로드 완료: {s3_uri}")
                return s3_uri
        
        raise Exception("응답에서 이미지 데이터를 찾을 수 없습니다.")
    
    except Exception as error:
        logger.error(f"이미지 생성 실패: {error}", exc_info=True)
        raise Exception(f"이미지 생성 중 오류 발생: {str(error)}")


async def generate_image(
    tool_context: ToolContext,
    prompt: str,
    aspect_ratio: str = "1:1",
    image_size: str = "1K"
) -> str:
    """
    텍스트 프롬프트로부터 이미지를 생성합니다.
    
    Args:
        prompt: 이미지 생성을 위한 상세한 영어 프롬프트. 구체적이고 명확한 시각적 요소를 포함해야 합니다.
        aspect_ratio: 이미지 종횡비 (1:1, 4:3, 16:9, 9:16). 기본값: 1:1
        image_size: 이미지 해상도 (1K, 2K). 기본값: 1K
    
    Returns:
        생성된 이미지 URI
    """
    # tool_context에서 user_id 추출
    user_id = tool_context.user_id
    
    # async 함수 실행
    return await _generate_image_async(
        prompt=prompt,
        user_id=user_id,
        aspect_ratio=aspect_ratio,
        image_size=image_size
    )
