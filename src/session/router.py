from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import service, schemas
from .dependencies import get_db
from src.runner.runner import get_session

router = APIRouter()


@router.post(
    "/create",
    response_model=schemas.SessionCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="세션 생성",
    description="새로운 세션을 생성합니다."
)
async def create_session(request: schemas.SessionCreateRequest, db: Session = Depends(get_db)):
    try:
        session = await get_session(
            user_id=request.user_id,
            session_id=None,
            state_config=request.metadata
        )
        if not session:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="세션을 생성할 수 없습니다.")
        return schemas.SessionCreateResponse(
            user_id=request.user_id,
            session_id=session.id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/list",
    response_model=schemas.SessionListResponse,
    status_code=status.HTTP_200_OK,
    summary="세션 목록 조회",
    description="세션 목록을 조회합니다."
)
async def list_sessions(user_id: str, db: Session = Depends(get_db)):
    try:
        sessions = service.get_list_sessions(db, user_id)
        return schemas.SessionListResponse(
            user_id=user_id,
            sessions=[schemas.SessionGetResponse(session_id=session.id) for session in sessions]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get(
    "/{session_id}",
    response_model=schemas.SessionGetResponse,
    status_code=status.HTTP_200_OK,
    summary="세션 조회",
    description="세션을 조회합니다."
)
async def get_single_session(session_id: str, db: Session = Depends(get_db)):
    try:
        session = service.get_single_session(db, session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="세션을 찾을 수 없습니다.")
        return schemas.SessionGetResponse(
            session_id=session.id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))