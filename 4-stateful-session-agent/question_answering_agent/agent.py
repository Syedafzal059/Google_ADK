from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

MODEL_GPT_4O = "openai/gpt-4o"


question_answering_agent = Agent(
    model = LiteLlm(model=MODEL_GPT_4O),
    name = 'question_answering_agent',
    description = 'question answering agent',
    instruction = """ 
    You are a helpful assistant that can answers questions about the user's preferences.
    Here is some information about the user:
    Name: {user_name}
    Preferences: {user_preferences}
    Answer the question based on the information provided.
    """,
    
)