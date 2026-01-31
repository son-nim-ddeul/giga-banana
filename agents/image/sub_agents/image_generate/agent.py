from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import types

from src.image.schemas import ImageResponse
from .prompt import description, instruction
from .tools.prompt_generator import prompt_generator_tool
from .tools.image_generator import generate_image


image_generate_agent = LlmAgent(
    name="image_generate_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(initial_delay=20, attempts=3)
    ),
    description=description,
    instruction=instruction,
    output_schema=ImageResponse,
    tools=[
        prompt_generator_tool,
        generate_image
    ]
)
