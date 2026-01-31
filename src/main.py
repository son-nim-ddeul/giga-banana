from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.session.router import router as session_router
from src.runner.runner import initialize_adk_services
from src.image.router import router as image_router
from src.bucket.router import router as bucket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # (필요시) 시작 시 실행할 코드
    initialize_adk_services()
    yield
    # (필요시) 종료 시 실행할 코드


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url=settings.docs_url,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


app.include_router(session_router, prefix="/sessions", tags=["Session"])
app.include_router(image_router, prefix="/images", tags=["Image"])
app.include_router(bucket_router, prefix="/bucket", tags=["Bucket"])

@app.get("/")
async def root():
    return {
        "message": "Giga Banana API",
        "version": settings.app_version,
    }
