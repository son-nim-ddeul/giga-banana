from google.adk.apps import App
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from src.image.schemas import ImageResponse

from .plugins.s3_url_presign import S3UrlPresignPlugin

root_agent = LlmAgent(
    name="image_specailist",
    model = Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=20, attempts=3)
    ),
    description="당신은 대화 전문가입니다. 유저의 질문에 대해 적절한 답변을 합니다.",
    instruction="당신은 대화 전문가입니다. 유저의 질문에 대해 적절한 답변을 합니다.",
    output_schema=ImageResponse
)

app = App(
    root_agent=root_agent, 
    name="image",
    plugins=[S3UrlPresignPlugin()]
)