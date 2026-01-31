from google.adk.agents import SequentialAgent
from google.adk.models import Gemini
from google.genai import types
from ...tools import read_workflow_creation_guide
from .tools import generate_image


image_generator_agent = SequentialAgent(
    name="image_generator",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=20, attempts=3)
    ),
    description="유저의 요청을 바탕으로 워크플로우를 생성 후 이미지를 생성합니다.",
    instruction="""
    1. 유저와의 대화를 통해 요구사항이 구체화되면 유저의 요청을 바탕으로 워크플로우를 생성합니다.
    2. 요구사항에 추가적인 요구사항이 있다면 추가적인 요구사항을 반환합니다.
    3. 워크플로우 생성 가이드를 참고하여 워크플로우를 생성합니다.
    4. 워크플로우 생성 후 이미지를 생성합니다.
    """,
    tools=[
        read_workflow_creation_guide,
        generate_image,
    ]
)
