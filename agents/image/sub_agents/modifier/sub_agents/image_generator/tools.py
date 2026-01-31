from pydantic import BaseModel
from google.adk.tools import ToolContext
import requests


class GeneratedImageResponse(BaseModel):
    user_id: str
    image_url: str


def generate_image(user_id: str, workflow: dict, ) -> GeneratedImageResponse:
    """
    이미지를 생성합니다.

    Args:
        user_id: str: 사용자 ID
        workflow: dict: 워크플로우

    Returns:
        GeneratedImageResponse: 이미지 생성 결과
    """
    url = "https://ui5lkk116duoen-8188.proxy.runpod.net/api/v2/workflow/run"
    request_body = {
        "user_id": user_id,
        "workflow": workflow
    }
    response = requests.post(url, json=request_body)
    return GeneratedImageResponse.model_validate_json(response.json())
