from datetime import datetime
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import google_search
from pydantic import BaseModel, Field, Json
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

MODEL_GPT_4O = "openai/gpt-4o"


class EmailContent(BaseModel):
    subject: str = Field(
        description = "The subject line of the email. Should be a short and concise subject line."
    )
    body: str = Field(
        description = "The body of the email. Should be a short, concise and well formated."
    )




root_agent = Agent(
    model = LiteLlm(model=MODEL_GPT_4O),
    name = 'email_assistant',
    description = 'A helpful assistant that can help with email content creation.',
    instruction = """ 
    You are a helpful assistant that can help with email content creation.
    You will be given a task and you need to create a email content for the task.
    You need to use the following JSON format for the email content:
    For example, if the task is "Write a email to the customer about the product", the email content should be:
    {
        "subject": "Product Inquiry",
        "body": "Dear [Customer Name],\n\nI hope this email finds you well. I am writing to inquire about the [product name] you offer. I am interested in learning more about its features and pricing. Please let me know if you have any information about this product. Thank you for your time and consideration.\n\nBest regards,\n[Your Name]"
    }
    do not include any other text in your response.
    """,
    output_schema = EmailContent,
    output_key = 'email',
)