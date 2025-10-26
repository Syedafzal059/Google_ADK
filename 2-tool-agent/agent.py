from datetime import datetime
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import google_search
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

MODEL_GPT_4O = "openai/gpt-4o"

def get_current_time()->dict:
    """Get the current time"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "current_time": now
    }


root_agent = Agent(
    model = LiteLlm(model=MODEL_GPT_4O),
    name = 'tool_agent',
    description = 'A helpful assistant that can use tools to answer user questions.',
    instruction = """ 
    You are a helpful assistant that can use following tools to answer user questions.
    - get_current_time: Use this tool to get the current time.
    """,
    #tools = [google_search],
    tools = [get_current_time],
)