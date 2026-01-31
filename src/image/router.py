from fastapi import APIRouter, status, HTTPException

from . import schemas
from src.runner.runner import setup_session_and_runner, execute_agent

router = APIRouter()

@router.post(
    "/run",
    response_model=schemas.ImageResponse,
    status_code=status.HTTP_200_OK,
    summary="이미지 생성/수정",
    description="이미지를 생성/수정합니다."
)
async def run_image(request: schemas.ImageRequest):
    try:
        session_id, runner = await setup_session_and_runner(request.user_id, request.session_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="세션을 찾을 수 없습니다.")

    try:
        response = await execute_agent(
            user_id=request.user_id,
            session_id=session_id,
            user_message=request.user_message,
            runner=runner,
            image_upload_url=request.image_upload_url,
            image_upload_mime_type=request.image_upload_mime_type
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))