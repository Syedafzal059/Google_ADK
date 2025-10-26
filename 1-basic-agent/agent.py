import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
import litellm
from IPython.display import IFrame
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys from environment variables
required_keys = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"), 
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY")
}

# Check for missing API keys
missing_keys = [key for key, value in required_keys.items() if not value]
if missing_keys:
    print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
    print("Please set these in your .env file or environment variables")
    print("At least one API key is required to run the agent")

# Set local URL
os.environ["AFZAL_LOCAL_URL"] = os.getenv("AFZAL_LOCAL_URL", "http://localhost:8888")
# Define model constants for cleaner code
MODEL_GEMINI_PRO = "gemini-1.5-pro"
MODEL_GPT_4O = "openai/gpt-4o"
MODEL_CLAUDE_SONNET = "anthropic/claude-3-sonnet-20240229"


root_agent = Agent(
    model=LiteLlm(model=MODEL_GPT_4O),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)


# IFrame for Jupyter notebook display (uncomment if running in Jupyter)
# IFrame(f"{os.environ.get('AFZAL_LOCAL_URL')}/terminal/4", width="600", height="768")