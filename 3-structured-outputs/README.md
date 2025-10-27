# Structured Outputs Agent

This example demonstrates how to create an agent with structured output using Google ADK. The agent generates email content in a consistent, predictable format.

## Overview

The agent uses **structured outputs** to ensure the LLM returns data in a specific, validated format. This is achieved through two key components:

### 1. `output_schema`

The `output_schema` parameter defines the expected structure and validation rules for the agent's output using Pydantic models.

**Key Points:**
- **Type Safety**: Ensures the output matches the defined structure
- **Validation**: Automatically validates the data before returning
- **Documentation**: Serves as inline documentation for the expected format
- **IDE Support**: Provides autocomplete and type hints in your code

**Example:**
```python
class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be a short and concise subject line."
    )
    body: str = Field(
        description="The body of the email. Should be a short, concise and well formated."
    )

root_agent = Agent(
    # ... other parameters ...
    output_schema = EmailContent,  # Defines the output structure
)
```

### 2. `output_key`

The `output_key` parameter specifies the key name under which the structured output will be stored in the agent's response.

**Key Points:**
- **Access Pattern**: Determines how you access the structured data
- **Response Organization**: Helps organize the response object
- **Consistency**: Provides a predictable way to retrieve data

**Example:**
```python
root_agent = Agent(
    # ... other parameters ...
    output_key = 'email',  # The output will be accessible via response['email']
)
```

When the agent runs, the structured output will be available as:
```python
response = await agent.run("Write an email about...")
email_content = response['email']  # Access via the output_key
# email_content.subject  # Access Pydantic fields
# email_content.body
```

## Why Include Output Structure in Instructions?

While `output_schema` provides the structure validation, **including the output structure in the `instruction` parameter is crucial** for several reasons:

### 1. **Model Guidance**
The LLM benefits from explicit examples and format descriptions in the instruction text. This helps the model understand the expected output better.

### 2. **Transparency**
It makes the expected output format clear to anyone reading the code, serving as documentation.

### 3. **Better Accuracy**
Explicit format instructions reduce hallucinations and improve the model's adherence to the desired structure.

### 4. **Example Format**
Providing an example JSON structure in the instruction gives the model a concrete template to follow:

```python
instruction = """ 
You are a helpful assistant that can help with email content creation.
You will be given a task and you need to create a email content for the task.
You need to use the following JSON format for the email content:
For example, if the task is "Write a email to the customer about the product", the email content should be:
{
    "subject": "Product Inquiry",
    "body": "Dear [Customer Name],..."
}
do not include any other text in your response.
"""
```

## Complete Example

```python
from pydantic import BaseModel, Field
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Define the structure
class EmailContent(BaseModel):
    subject: str = Field(description="The subject line of the email.")
    body: str = Field(description="The body of the email.")

# Create the agent
root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='email_assistant',
    description='A helpful assistant that can help with email content creation.',
    instruction="""
    You will create email content in the following format:
    {
        "subject": "...",
        "body": "..."
    }
    """,
    output_schema=EmailContent,  # Pydantic model for validation
    output_key='email',          # Response key name
)
```

## Benefits of Structured Outputs

1. **Type Safety**: Catch errors at development time
2. **Consistency**: Always get data in the expected format
3. **Documentation**: Self-documenting code with Pydantic models
4. **Validation**: Automatic data validation
5. **IDE Support**: Better autocomplete and type checking
6. **Error Handling**: Validation errors are clearly communicated

## Usage

Run the agent with a prompt to get structured output:

```python
result = await root_agent.run("Write an email to a client about a new product launch")
print(result['email'].subject)  # Access structured fields
print(result['email'].body)
```

