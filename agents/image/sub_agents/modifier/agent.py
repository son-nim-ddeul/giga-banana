from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from agents.image.sub_agents.modifier.sub_agents.image_generator.agent import image_generator_agent
from .tools import (
    read_user_interaction_nodes_info,
    read_user_interaction_node_details,
    read_workflow_creation_guide,
    read_checkpoint_summary,
    read_checkpoint_info_details,
)


agent = LlmAgent(
    name="image_modifier",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=20, attempts=3)
    ),
    description="당신은 stable diffusion 워크플로우를 생성하는 전문가입니다. 유저의 요청을 바탕으로 이미지를 수정하기 위한 워크플로우를 생성합니다.",
    instruction="""
    ## 전제
    - 유저는 스테이블 디퓨전(이미지 생성/수정 도구)에 대한 지식이 없거나 부족한 상황을 가정합니다.
    - 단순한 요구사항일 경우 구체화할지, 그대로 진행할지 결정합니다.
    - 리액션 금지, 반복되는 확인 금지.
    - 짧고 명확하게 요구사항을 파악합니다.

    ## 요구사항 구체화 (대화 단계)
    1. 유저의 말을 듣고, **유저 상호작용용 노드** 문서(유저에게 값을 받을 수 있는 노드만)를 참고하여 "실제로 무엇을 할 수 있는지"를 파악합니다.
    2. 유저에게는 전문 용어(노드, 체크포인트, 워크플로우, LoRA, ControlNet 등)를 쓰지 않고, 쉽고 일상적인 단어 위주로 질문하고 설명합니다.
    3. 요구사항이 명확해질 때까지 대화를 이어갑니다.
    4. 최종 요구사항이 정리되면, 유저가 이해하기 쉬운 문장으로 전체 요구사항을 정리해서 보여줍니다.

    ## 워크플로우 생성
    5. 정리된 요구사항과 체크포인트 정보를 바탕으로 image_generator에게 워크플로우 생성을 위임합니다. (워크플로우 최적화·내부 구조용 노드는 image_generator가 별도로 참고합니다.)
    """,
    tools=[
        read_user_interaction_nodes_info,
        read_user_interaction_node_details,
        read_workflow_creation_guide,
        read_checkpoint_summary,
        read_checkpoint_info_details,
        AgentTool(image_generator_agent, skip_summarization=True),
    ],
)
