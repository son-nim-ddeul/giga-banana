import logging
from google.adk.tools.tool_context import ToolContext

from google import genai
from google.genai import types

from src.bucket.manager import S3BucketManager
from src.config import settings

logger = logging.getLogger(__name__)

# 시스템 프롬프트: 이미지 수정 가이드라인
IMAGE_EDIT_SYSTEM_PROMPT = """
You are an expert AI image editing assistant.
Edit and modify images based on the provided instructions while preserving specified elements.
Focus on:
- Maintaining consistency with preserved elements (faces, poses, identities)
- Natural integration of changes with existing elements
- Professional quality output
- Accurate interpretation of edit instructions
- Seamless blending of modified and preserved areas
"""


async def _edit_image_async(
    original_image_url: str,
    edit_prompt: str,
    user_id: str,
    aspect_ratio: str = "1:1",
    image_size: str = "1K"
) -> str:
    """
    Gemini API를 사용하여 이미지 수정 및 S3 업로드 (내부 async 함수)
    
    Args:
        original_image_url: 원본 이미지 S3 URI (s3://giga-banana/...)
        edit_prompt: 이미지 수정 프롬프트
        user_id: 사용자 ID
        aspect_ratio: 출력 이미지 종횡비
        image_size: 출력 이미지 해상도
        
    Returns:
        수정된 이미지의 S3 URI
    """
    
    if not settings.google_api_key:
        raise Exception("GOOGLE_API_KEY가 설정되지 않았습니다.")
    
    try:
        logger.info(f"이미지 수정 시작 - user_id: {user_id}, original: {original_image_url}")
        
        # Presigned URL 또는 일반 HTTP URL이 온 경우 처리
        if original_image_url.startswith("http://") or original_image_url.startswith("https://"):
            # Gemini 내부 URL 감지 (접근 불가능)
            if "model-garden.gemini.run" in original_image_url or "gemini.run" in original_image_url:
                raise Exception(
                    f"Gemini 내부 임시 URL은 사용할 수 없습니다. "
                    f"이미지를 다시 업로드하거나 S3에 저장된 이미지를 사용해주세요. "
                    f"URL: {original_image_url}"
                )
            
            # S3 presigned URL인 경우 S3 URI로 변환 시도
            if "giga-banana.s3" in original_image_url or "s3.ap-northeast-2.amazonaws.com/giga-banana" in original_image_url:
                logger.info(f"S3 presigned URL 감지. S3 URI로 변환 시도")
                from urllib.parse import urlparse
                parsed = urlparse(original_image_url)
                # URL path에서 키 추출 (예: /giga-banana/images/user/file.jpg 또는 /images/user/file.jpg)
                path = parsed.path
                if path.startswith("/giga-banana/"):
                    key = path[len("/giga-banana/"):]
                elif path.startswith("/"):
                    key = path[1:]  # 첫 슬래시 제거
                else:
                    key = path
                
                s3_uri = f"s3://giga-banana/{key}"
                logger.info(f"Presigned URL을 S3 URI로 변환: {s3_uri}")
                original_image_url = s3_uri
        
        # S3 URI 또는 HTTP URL 처리
        if original_image_url.startswith("s3://giga-banana/"):
            # S3 URI인 경우 정상 처리
            bucket_manager = S3BucketManager()
            logger.info(f"S3 다운로드 시도 중: {original_image_url}")
            original_image_data = await bucket_manager.download_file(file_uri=original_image_url)
            logger.info(f"원본 이미지 다운로드 완료 ({len(original_image_data)} bytes)")
        elif original_image_url.startswith("http://") or original_image_url.startswith("https://"):
            logger.warning(f"일반 HTTP URL에서 직접 다운로드 시도: {original_image_url}")
            # 일반 HTTP URL에서 직접 다운로드
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(original_image_url) as response:
                    response.raise_for_status()
                    original_image_data = await response.read()
                    logger.info(f"HTTP URL에서 이미지 다운로드 완료 ({len(original_image_data)} bytes)")
        else:
            raise Exception(f"지원하지 않는 이미지 URL 형식입니다. S3 URI 또는 HTTP(S) URL이어야 합니다. 받은 값: {original_image_url}")
        
        # S3BucketManager는 업로드용으로 다시 필요
        bucket_manager = S3BucketManager()
        
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=settings.google_api_key)
        
        # API 요청 콘텐츠 구성: 원본 이미지 바이너리 + 수정 프롬프트
        contents = [
            types.Part.from_bytes(
                data=original_image_data,
                mime_type="image/jpeg"
            ),
            types.Part.from_text(text=edit_prompt)
        ]
        
        # 생성 설정
        config = types.GenerateContentConfig(
            system_instruction=IMAGE_EDIT_SYSTEM_PROMPT,
            temperature=1.0,
            candidate_count=1,
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size
            )
        )
        
        # Gemini API 호출 (image_generator와 동일한 모델)
        logger.info("Gemini API 호출 중 (이미지 수정)...")
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=config
        )
        
        logger.info(f"Gemini 응답 수신")
        
        # 응답 처리
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                logger.info(f"텍스트 응답: {part.text}")
            elif part.inline_data is not None:
                # 수정된 이미지 데이터 처리
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type
                
                # S3 업로드 (async) - edited prefix로 저장
                s3_uri = await bucket_manager.upload_file(
                    user_id=user_id,
                    file_data=image_data,
                    mime_type=mime_type,
                    file_name=f"edited_{__import__('uuid').uuid4()}"
                )
                
                logger.info(f"수정된 이미지 S3 업로드 완료: {s3_uri}")
                
                # Creations 테이블에 저장
                from src.database.session import RDS_Session
                from src.session.service import create_creation
                
                db = RDS_Session()
                try:
                    create_creation(
                        db=db,
                        user_id=user_id,
                        image_url=s3_uri,
                        workflow=None,
                        creation_metadata={
                            "type": "edit",
                            "original_image": original_image_url,
                            "edit_prompt": edit_prompt
                        }
                    )
                    logger.info(f"Creation record saved for edited image: {s3_uri}")
                except Exception as db_error:
                    logger.error(f"Failed to save creation record: {db_error}", exc_info=True)
                    # DB 저장 실패해도 S3 URI는 반환 (이미지는 수정됨)
                finally:
                    db.close()
                
                return s3_uri
        
        raise Exception("응답에서 수정된 이미지 데이터를 찾을 수 없습니다.")
    
    except Exception as error:
        logger.error(f"이미지 수정 실패: {error}", exc_info=True)
        raise Exception(f"이미지 수정 중 오류 발생: {str(error)}")


async def edit_image(
    tool_context: ToolContext,
    edit_prompt: str,
    aspect_ratio: str = "1:1",
    image_size: str = "1K"
) -> str:
    """
    기존 이미지를 수정 프롬프트에 따라 편집합니다.
    
    현재 세션의 최근 메시지에서 업로드된 이미지를 자동으로 감지하여 수정합니다.
    
    Args:
        edit_prompt: 이미지 수정을 위한 상세한 영어 프롬프트. 
                     보존할 요소("Keep ... unchanged")와 변경할 요소를 명확히 포함해야 합니다.
        aspect_ratio: 이미지 종횡비 (1:1, 4:3, 16:9, 9:16). 기본값: 1:1
        image_size: 이미지 해상도 (1K, 2K). 기본값: 1K
    
    Returns:
        수정된 이미지의 S3 URI
    """
    # tool_context에서 user_id 추출
    user_id = tool_context.user_id
    
    # 세션의 최근 이벤트에서 이미지 file_uri 찾기
    original_image_url = None
    session = tool_context.session
    
    # 최근 이벤트부터 역순으로 탐색
    for event in reversed(session.events):
    # user role과 model role 모두 확인 (사용자 업로드 + 생성된 이미지)
        if event.content and event.content.role in ['user', 'model']:
            if hasattr(event.content, 'parts') and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'file_data') and part.file_data:
                        file_uri = getattr(part.file_data, 'file_uri', None)
                        if file_uri:
                            original_image_url = file_uri
                            logger.info(f"세션 이벤트에서 이미지 감지 (role={event.content.role}): {file_uri}")
                            break
            if original_image_url:
                break
    
    if not original_image_url:
        raise Exception(
            "수정할 이미지를 찾을 수 없습니다. "
            "이미지를 업로드한 후 수정 요청을 해주세요."
        )
    
    # async 함수 실행
    return await _edit_image_async(
        original_image_url=original_image_url,
        edit_prompt=edit_prompt,
        user_id=user_id,
        aspect_ratio=aspect_ratio,
        image_size=image_size
    )
