from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types

from src.image.schemas import ImageResponse
from .prompt import description, instruction
from .tools.edit_prompt_generator import edit_prompt_generator_tool
from .tools.image_editor import edit_image


image_edit_agent = LlmAgent(
    name="image_edit_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=10, attempts=10)
    ),
    description=description,
    instruction=instruction,
    output_schema=ImageResponse,
    tools=[
        edit_prompt_generator_tool,
        edit_image
    ]
)
