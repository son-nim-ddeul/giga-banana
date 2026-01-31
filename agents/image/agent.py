from google.adk.apps import App
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .plugins.s3_url_presign import S3UrlPresignPlugin

from .prompt import (
    image_specailist_description,
    image_specailist_instruction
)

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.genai.types import Content, Part
from typing import Optional
import json

# TODO : test 용
def simple_after_model_modifier(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    # LLM의 원본 응답 텍스트 추출
    if llm_response.content and llm_response.content.parts:
        original_text = ""
        for part in llm_response.content.parts:
            if part.text:
                original_text += part.text
        
        # 원하는 형식으로 JSON 변환
        response_json = {
            "response_message": original_text,
            "response_image_url": None
        }
        
        # JSON 문자열로 변환
        json_text = json.dumps(response_json, ensure_ascii=False)
        
        # 새로운 응답 생성 (Part 객체 직접 생성)
        llm_response.content = Content(
            role='model',
            parts=[types.Part(text=json_text)]
        )
    
    return llm_response

root_agent = LlmAgent(
    name="image_specailist",
    model = Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=20, attempts=3)
    ),
    description="당신은 대화 전문가입니다. 유저의 질문에 대해 적절한 답변을 합니다.",
    instruction="당신은 대화 전문가입니다. 유저의 질문에 대해 적절한 답변을 합니다.",
    after_model_callback=simple_after_model_modifier,
)

app = App(
    root_agent=root_agent, 
    name="image",
    plugins=[S3UrlPresignPlugin()]
)