import logging
import json
from typing import Any, Optional

from google.adk.runners import Runner
from google.adk.sessions import Session
from google.genai import types
from google.genai.types import Content, Part
from google.adk.sessions.database_session_service import DatabaseSessionService
from src.config import settings
from agents.image.agent import app as image_app

logger = logging.getLogger(__name__)

_runners: dict[str, Runner] = {}
_session_service: DatabaseSessionService | None = None


def initialize_adk_services():
    """ADK 서비스 초기화 (FastAPI lifespan에서 호출)"""
    global _session_service, _runners
    
    # SessionService 초기화
    db_url = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
    _session_service = DatabaseSessionService(db_url=db_url)
    
    # Runner 초기화
    _runners[image_app.name] = Runner(app=image_app, session_service=_session_service)


def get_session_service() -> DatabaseSessionService:
    """SessionService 싱글턴 가져오기"""
    if _session_service is None:
        raise RuntimeError("SessionService not initialized. Call initialize_adk_services() first.")
    return _session_service


def get_runner(app_name: str) -> Runner:
    """Runner 싱글턴 가져오기"""
    if app_name not in _runners:
        raise ValueError(f"지원되지 않는 app_name: {app_name}")
    return _runners[app_name]


async def get_session(
    user_id: str,
    session_id: Optional[str] = None,
    state_config: Optional[dict[str, Any]] = None
) -> Session:
    session_service = get_session_service()
    if session_id:
        session = await session_service.get_session(
            app_name=image_app.name,
            user_id=user_id,
            session_id=session_id
        )
    else:
        session = await session_service.create_session(
            app_name=image_app.name,
            state=state_config,
            user_id=user_id
        )
        if not session:
            raise Exception(f"세션을 찾을 수 없습니다. session_id={session_id}")
    return session


async def setup_session_and_runner(
    user_id: str,
    session_id: str | None = None,
    state_config: dict[str, Any] = {}
) -> tuple[str, Runner]:
    """
    세션과 Runner를 설정합니다.
    Runner는 캐싱된 싱글턴을 사용합니다.
    """
    runner = get_runner(image_app.name)
    session = get_session(
        user_id=user_id,
        session_id=session_id,
        state_config=state_config
    )
    return session.id, runner

def _create_file_data_part(
    file_uri: str, 
    mime_type: str
) -> types.Part:
    """file_data Part 생성"""
    return types.Part.from_uri(
        uri=file_uri,
        mime_type=mime_type
    )

async def execute_agent(
    user_id: str,
    session_id: str,
    user_message: str,
    runner: Runner,
    image_upload_url: str | None = None,
    image_upload_mime_type: str | None = None
) -> dict[str, Any]:
    parts = [Part.from_text(text=user_message)]
    if image_upload_url and image_upload_mime_type:
        parts.append(_create_file_data_part(image_upload_url, image_upload_mime_type))
    execute_message = Content(role = 'user', parts=parts)

    final_response_content = {
        "response_message": "이미지 생성/수정 결과가 없습니다.",
        "response_image_url": None
    }
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=execute_message):
            if event.is_final_response() and event.content and event.content.parts:
                # For output_schema, the content is the JSON string itself
                final_response_content = event.content.parts[0].text

        if not final_response_content:
            return final_response_content

        return json.loads(final_response_content)
    except Exception as e:
        logger.exception("Error in execute_agent: %s", e)
        error_message = str(e) if str(e) else "에이전트 동작간 예외가 발생하였습니다."

        return {
            "response_message": error_message,
            "response_image_url": None
        }
