# 2-Tool-Agent

This agent demonstrates how to create and use custom tools with Google ADK.

## Overview

The `tool_agent` is equipped with custom tools that extend its capabilities beyond basic LLM responses.

## Features

- **Custom Tool Integration**: Uses custom `get_current_time` tool to retrieve current date and time
- **Tool-based Instructions**: Agent is provided with clear instructions on how to use available tools
- **Extensible Design**: Easy to add more tools as needed

## Tools Available

### 1. `get_current_time`
A custom tool that returns the current date and time in `YYYY-MM-DD HH:MM:SS` format.

**Usage Example:**
- User: "What time is it?"
- Agent: Calls `get_current_time()` and responds with the current timestamp

## Code Structure

```python
def get_current_time() -> dict:
    """Get the current time"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": now}

root_agent = Agent(
    model=LiteLlm(model=MODEL_GPT_4O),
    name='tool_agent',
    description='A helpful assistant that can use tools...',
    instruction=""" 
    You are a helpful assistant that can use following tools...
    - get_current_time: Use this tool to get the current time.
    """,
    tools=[get_current_time],
)
```

## Adding More Tools

To add additional tools to this agent:

1. Create a new tool function
2. Add it to the `tools` list in the Agent configuration
3. Update the `instruction` field to include usage information for the new tool

**Example - Adding a new tool:**

```python
def calculate_sum(a: int, b: int) -> dict:
    """Calculate the sum of two numbers"""
    return {"result": a + b}

root_agent = Agent(
    # ... existing config ...
    tools=[get_current_time, calculate_sum],
)
```

## Running the Agent

From the root directory:

```bash
adk web
```

Then select the `2-tool-agent` to interact with this agent.

## Notes

- The `google_search` tool is commented out but can be enabled by uncommenting line 30
- Tools should return dictionaries for consistent integration with the ADK
- Document tool functions with docstrings to help the agent understand when to use them

## Next Steps

Consider adding more useful tools such as:
- Calculator functions
- Data validation
- External API calls
- File operations (with proper permissions)

