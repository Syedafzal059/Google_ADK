# Stateful Session Agent

This example demonstrates how to create and manage **stateful sessions** with Google ADK. The agent maintains conversation context and user-specific state across multiple interactions.

## Overview

Stateful sessions allow agents to:
- **Remember context** across multiple conversations
- **Store user-specific data** that persists between interactions
- **Maintain conversation history** automatically
- **Access state variables** in agent instructions dynamically

## Key Concepts

### 1. Session Service (`InMemorySessionService`)

The session service manages session creation, retrieval, and state storage. It provides both async and sync methods:

**Synchronous Methods (for simple scripts):**
```python
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()

# Create a session
session = session_service.create_session_sync(
    app_name="My App",
    user_id="user123",
    session_id="session456",
    state={"key": "value"}
)

# Retrieve a session
session = session_service.get_session_sync(
    app_name="My App",
    user_id="user123",
    session_id="session456"
)
```

**Asynchronous Methods (recommended):**
```python
# Create a session
session = await session_service.create_session(
    app_name="My App",
    user_id="user123",
    session_id="session456",
    state={"key": "value"}
)

# Retrieve a session
session = await session_service.get_session(
    app_name="My App",
    user_id="user123",
    session_id="session456"
)
```

### 2. Session State

Session state is a dictionary that stores user-specific information. This state can be:
- **Initialized** when creating a session
- **Accessed** in agent instructions using template variables
- **Updated** during conversation (via state deltas)
- **Retrieved** after interactions

**State Structure:**
```python
initial_state = {
    "user_name": "Afzal",
    "user_preferences": """
        I like cricket and I like to play cricket.
        I am an Agentic AI Developer
        I am from India"""
}
```

### 3. State Injection in Instructions

State variables can be dynamically injected into agent instructions using curly brace syntax `{variable_name}`:

```python
question_answering_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='question_answering_agent',
    instruction = """ 
    You are a helpful assistant that can answers questions about the user's preferences.
    Here is some information about the user:
    Name: {user_name}
    Preferences: {user_preferences}
    Answer the question based on the information provided.
    """,
)
```

**Key Points:**
- Variables in `{curly_braces}` are automatically replaced with state values
- If a variable doesn't exist in state, a `KeyError` will be raised
- State variables are case-sensitive and must match exactly

### 4. Runner with Session Service

The `Runner` connects the agent to the session service, enabling stateful conversations:

```python
from google.adk.runners import Runner

runner = Runner(
    agent=question_answering_agent,
    app_name="My App",
    session_service=session_service,
)
```

When running the agent, you must provide:
- `user_id`: Identifies the user
- `session_id`: Identifies the specific session
- `new_message`: The user's message

```python
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response:
        print(event.content.parts[0].text)
```

## Complete Example

```python
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from uuid import uuid4
from google.genai import types

# Initialize session service
session_service = InMemorySessionService()

# Define initial state
initial_state = {
    "user_name": "Afzal",
    "user_preferences": "I like cricket and I am an AI Developer"
}

# Create a session
APP_NAME = "Afzal's AI Assistant"
USER_ID = "afzal"
SESSION_ID = str(uuid4())

session = session_service.create_session_sync(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)

# Create runner with session service
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# Run the agent with session context
new_message = types.Content(
    role="user",
    parts=[types.Part(text="What is Afzal's favorite sport?")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response:
        print(f"Response: {event.content.parts[0].text}")

# Retrieve and inspect session state
session = session_service.get_session_sync(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

print("Session State:")
for key, value in session.state.items():
    print(f"{key}: {value}")
```

## State Management

### State Types

Google ADK supports three types of state:

1. **Session State**: Specific to a single session
   - Stored in `session.state`
   - Accessible via `{variable_name}` in instructions
   - Example: `{"user_name": "Afzal"}`

2. **User State**: Shared across all sessions for a user
   - Prefixed with `user:` in the state dictionary
   - Persists across multiple sessions for the same user
   - Example: `{"user:preferences": "..."}`

3. **App State**: Shared across all users and sessions
   - Prefixed with `app:` in the state dictionary
   - Global to the application
   - Example: `{"app:version": "1.0"}`

### State Updates

State can be updated during conversations through state deltas in agent actions. The session service automatically merges these updates.

## Benefits of Stateful Sessions

1. **Context Preservation**: Agents remember previous conversations
2. **Personalization**: User-specific data enables personalized responses
3. **Efficiency**: No need to re-provide context in every message
4. **Scalability**: State management is handled automatically
5. **Flexibility**: Mix of session, user, and app-level state

## Common Patterns

### Pattern 1: User Profile Management
```python
initial_state = {
    "user_name": "John",
    "user_role": "Developer",
    "user_preferences": "Prefers Python over Java"
}
```

### Pattern 2: Conversation Context
```python
initial_state = {
    "conversation_topic": "Technical Support",
    "previous_issues": ["Login problem", "API error"],
    "user_satisfaction": "High"
}
```

### Pattern 3: Multi-turn Conversations
```python
# First interaction
runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=message1)

# Later interaction - state persists
runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=message2)
```

## Error Handling

### Common Errors

1. **KeyError: Context variable not found**
   - **Cause**: Variable in instruction template doesn't exist in state
   - **Solution**: Ensure state keys match instruction variables exactly

2. **Session not found**
   - **Cause**: Session ID doesn't exist or was deleted
   - **Solution**: Create the session before using it

3. **AlreadyExistsError**
   - **Cause**: Trying to create a session with an existing ID
   - **Solution**: Use a new session_id or check if session exists first

## Running the Example

From the `4-stateful-session-agent` directory:

```bash
python basic_stateful_session.py
```

This will:
1. Create a new session with initial state
2. Run the agent with a question
3. Display the agent's response
4. Show the final session state

## Next Steps

Consider exploring:
- **State Updates**: How to modify state during conversations
- **Session Lifecycle**: Creating, updating, and deleting sessions
- **Multi-User Scenarios**: Managing sessions for multiple users
- **State Persistence**: Using persistent session services (not in-memory)
- **Event History**: Accessing conversation history from sessions
