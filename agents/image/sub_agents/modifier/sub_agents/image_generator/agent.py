from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types
from ...tools import (
    read_workflow_creation_guide,
    read_optimization_nodes_info,
    read_optimization_node_details,
)
from .tools import generate_image, extract_image_prompt


image_generator_agent = LlmAgent(
    name="image_generator",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=20, attempts=3)
    ),
    description="유저의 요청을 바탕으로 워크플로우를 생성 후 이미지를 생성합니다.",
    instruction="""
    1. 유저와의 대화를 통해 요구사항이 구체화되면 유저의 요청을 바탕으로 워크플로우를 생성합니다.
    2. 요구사항에 추가적인 요구사항이 있다면 추가적인 요구사항을 반환합니다.
    3. 워크플로우 생성 가이드와 **워크플로우 최적화 노드** 문서(파이프라인·유틸·메타데이터·패턴)를 참고하여 워크플로우를 구성·최적화합니다.
    4. 워크플로우의 프롬프트 작성 후 원본 이미지의 프롬프트(태그)를 추가합니다.
    5. 워크플로우 생성 후 이미지를 생성합니다.
    """,
    tools=[
        read_workflow_creation_guide,
        read_optimization_nodes_info,
        read_optimization_node_details,
        generate_image,
        extract_image_prompt,
    ]
)
