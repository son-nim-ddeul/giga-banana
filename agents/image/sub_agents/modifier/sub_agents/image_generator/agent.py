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
    1. 유저와의 대화에서 워크플로우를 생성합니다.
    2. 커스텀 노드를 탐색해서 요구사항에 부합한 노드를 찾습니다.
    3. 커스텀 노드에 필요한 정보를 유저에게 묻습니다. 필요한 질문은 한번에 하고 불충분한 답이 와도 추가 질문을 하지 않습니다. 불충분한 데이터는 임의의 값으로 설정합니다.
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
