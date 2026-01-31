# TODO : 작성 필요
image_specailist_description = """

"""

image_specailist_instruction = """

"""


# agent 구성 계획
"""
1. root_agent
- 사용자의 요청을 받아 적절한 에이전트로 연결하고 작업을 분배합니다.

- sub_agents
 1. image generate specailist
 - 사용자의 요청을 받아 이미지를 생성합니다. 사용자가 이미지를 첨부하지 않고 이미지를 생성 요청하는 경우에 역할을 수행합니다
 2. image edit specailist
 - 사용자의 요청을 받아 이미지를 수정합니다. 사용자가 이미지를 첨부하고 이미지를 수정 요청하는 경우에 역할을 수행합니다

2. image generate specailist
- 사용자의 요청을 바탕으로 이미지 생성을 위한 프롬프트를 작성 후, 이미지를 생성합니다.

3. image edit specailist
- 사용자의 요청을 바탕으로 이미지 수정을 위한 프롬프트를 작성 후, 이미지를 수정합니다.

- 수정은 stable diffusion 워크플로우를 사용하여 수정합니다.
-> a. 사용자 요청 피드백 specailist
-> b. 이미지 수정 specailist
"""