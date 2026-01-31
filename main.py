"""
FastAPI 서버 실행 파일
"""
import uvicorn

from src.config import settings


def main():
    """서버 실행"""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
