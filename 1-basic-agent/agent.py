import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MODEL_GPT_4O = "openai/gpt-4o"

root_agent = Agent(
    model=LiteLlm(model=MODEL_GPT_4O),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)


