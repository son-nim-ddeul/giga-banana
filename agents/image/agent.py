from google.adk.apps import App
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .plugins.s3_url_presign import S3UrlPresignPlugin
from .sub_agents.image_generate.agent import image_generate_agent
# from .sub_agents.modifier.agent import agent as image_modifier_agent
from .sub_agents.editer.agent import image_edit_agent as image_editer_agent
from .prompt import description, instruction

root_agent = LlmAgent(
    name="image_specialist",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=10, attempts=10)
    ),
    description=description,
    instruction=instruction,
    sub_agents=[
        image_generate_agent,
        # image_modifier_agent,
        image_editer_agent
    ]
)

app = App(
    root_agent=root_agent, 
    name="image",
    plugins=[S3UrlPresignPlugin()]
)