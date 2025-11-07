# Persistent Memory Agent

This example demonstrates how to create and manage **persistent memory** with Google ADK using `DatabaseSessionService`. Unlike in-memory storage, persistent memory survives application restarts, allowing agents to remember conversations and user data across sessions.

## Overview

Persistent memory enables agents to:
- **Remember data across restarts** - All state is saved to a database file
- **Maintain long-term context** - Conversations and user preferences persist indefinitely
- **Support production deployments** - Data survives server restarts and deployments
- **Enable session continuity** - Users can resume conversations after closing the application

## Key Concepts

### 1. Session Service (`DatabaseSessionService`)

The `DatabaseSessionService` manages session creation, retrieval, and state storage in a database. It provides async methods for persistent storage:

**Asynchronous Methods (required for database operations):**
```python
from google.adk.sessions.database_session_service import DatabaseSessionService

# Initialize with SQLite database
db_url = "sqlite:///my_agent_database.db"
session_service = DatabaseSessionService(db_url=db_url)

# Create a session
session = await session_service.create_session(
    app_name="My App",
    user_id="user123",
    state={"key": "value"}
)

# Retrieve a session
session = await session_service.get_session(
    app_name="My App",
    user_id="user123",
    session_id=session.id
)

# List existing sessions
existing_sessions = await session_service.list_sessions(
    app_name="My App",
    user_id="user123"
)
```

**Key Difference from InMemorySessionService:**
- Data persists to a database file (SQLite by default)
- Survives application restarts
- Suitable for production use
- Slightly slower but permanent

### 2. Session State

Session state is a dictionary that stores user-specific information. This state is **automatically persisted** to the database:

**State Structure:**
```python
initial_state = {
    "user_name": "Afzal",
    "reminders": []
}
```

**State Persistence:**
- State is saved to the database when sessions are created
- State updates via `state_delta` are automatically persisted
- State survives application restarts

### 3. State Injection in Instructions

State variables can be dynamically injected into agent instructions using curly brace syntax `{variable_name}`:

```python
memory_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='memory_agent',
    instruction = """ 
    You are a smart reminder agent with persistent storage.

    The user's information is stored in the session state.
    -User's name: {user_name}
    -Reminders: {reminders}
    You can use the following tools to manage the user's reminders:
    - add_reminder: Add a reminder to the user's list of reminders
    - view_reminders: View the user's list of reminders
    - delete_reminder: Delete a reminder from the user's list of reminders
    - update_reminder: Update a reminder in the user's list of reminders
    - update_user_name: Update the user's name
    """,
)
```

**Key Points:**
- Variables in `{curly_braces}` are automatically replaced with state values
- If a variable doesn't exist in state, a `KeyError` will be raised
- State variables are case-sensitive and must match exactly

### 4. Runner with Session Service

The `Runner` connects the agent to the session service, enabling stateful conversations with persistence:

```python
from google.adk.runners import Runner

runner = Runner(
    agent=memory_agent,
    app_name="My App",
    session_service=session_service,
)
```

When running the agent, you must provide:
- `user_id`: Identifies the user
- `session_id`: Identifies the specific session
- `new_message`: The user's message

```python
async for event in runner.run_async(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response:
        print(event.content.parts[0].text)
```

## Complete Example

```python
import asyncio
from dotenv import load_dotenv
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.adk.runners import Runner
from utils import call_agent_async
from memory_agent.agent import memory_agent

load_dotenv()

# Initialize persistent storage
db_url = "sqlite:///my_agent_database.db"
session_service = DatabaseSessionService(db_url=db_url)

# Define initial state
initial_state = {
    "user_name": "Afzal",
    "reminders": [],
}

async def main():
    APP_NAME = "Afzal's AI Assistant"
    USER_ID = "afzal"
    
    # Check for existing session (persists across restarts)
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Resuming existing session: {SESSION_ID}")
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"New session created: {SESSION_ID}")
    
    # Create runner with session service
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    # Interactive loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Ending conversation... Your data has been saved.")
            break
        
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

if __name__ == "__main__":
    asyncio.run(main())
```

## State Management

### State Types

Google ADK supports three types of state, all of which are persisted to the database:

1. **Session State**: Specific to a single session
   - Stored in `session.state`
   - Accessible via `{variable_name}` in instructions
   - Persisted to database
   - Example: `{"user_name": "Afzal", "reminders": []}`

2. **User State**: Shared across all sessions for a user
   - Prefixed with `user:` in the state dictionary
   - Persists across multiple sessions for the same user
   - Example: `{"user:preferences": "..."}`

3. **App State**: Shared across all users and sessions
   - Prefixed with `app:` in the state dictionary
   - Global to the application
   - Example: `{"app:version": "1.0"}`

### State Updates with Persistence

State can be updated during conversations through state deltas. **Use `state_delta` to ensure persistence:**

```python
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a reminder - automatically persisted to database"""
    reminders = tool_context.session.state.get("reminders", [])
    reminders.append(reminder)
    
    # Use state_delta to ensure persistence
    tool_context.actions.state_delta = {"reminders": reminders}
    
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Reminder '{reminder}' added successfully"
    }
```

**Key Points:**
- `tool_context.actions.state_delta` ensures changes are persisted to the database
- Direct modifications to `tool_context.session.state` update in-memory state but may not persist immediately
- State deltas are automatically saved when events are appended to the session

## Benefits of Persistent Memory

1. **Data Durability**: Data survives crashes, restarts, and deployments
2. **Long-term Memory**: Agents remember users across weeks or months
3. **Production Ready**: Suitable for real-world applications
4. **Session Continuity**: Users can resume conversations after closing the app
5. **Backup and Recovery**: Database files can be backed up and restored

## Common Patterns

### Pattern 1: Session Reuse Across Restarts
```python
# Check for existing session before creating new one
existing_sessions = await session_service.list_sessions(
    app_name=APP_NAME,
    user_id=USER_ID,
)

if existing_sessions and len(existing_sessions.sessions) > 0:
    SESSION_ID = existing_sessions.sessions[0].id
    # Resume existing session with all previous data
else:
    # Create new session only if none exists
    new_session = await session_service.create_session(...)
```

### Pattern 2: Reminder Management with Persistence
```python
initial_state = {
    "user_name": "John",
    "reminders": []  # This list persists across restarts
}

# User adds reminders
# Data is saved to database
# Next time app starts, reminders are still there
```

### Pattern 3: State Updates with Persistence
```python
# In tool functions, use state_delta for persistence
tool_context.actions.state_delta = {
    "reminders": updated_reminders,
    "user_name": new_name
}
```

## Database File Location

The database file is created in the current working directory by default:

**Relative Path (3 slashes):**
```python
db_url = "sqlite:///my_agent_database.db"
# Creates: ./my_agent_database.db (in current working directory)
```

**Finding Your Database:**
```python
import os
from sqlalchemy import create_engine

db_url = "sqlite:///my_agent_database.db"
engine = create_engine(db_url)
actual_path = os.path.abspath(engine.url.database)
print(f"Database location: {actual_path}")
```

## Error Handling

### Common Errors

1. **KeyError: Context variable not found**
   - **Cause**: Variable in instruction template doesn't exist in state
   - **Solution**: Ensure state keys match instruction variables exactly

2. **Session not found**
   - **Cause**: Session ID doesn't exist or was deleted
   - **Solution**: Check for existing sessions using `list_sessions()` before creating new ones

3. **Database connection errors**
   - **Cause**: Database file locked or path incorrect
   - **Solution**: Check database file permissions and path format

4. **State not persisting**
   - **Cause**: Not using `state_delta` in tools
   - **Solution**: Use `tool_context.actions.state_delta` instead of direct state modification

## Running the Example

From the `5-persistent-storage-agent` directory:

```bash
python main.py
```

**First Run:**
- Creates a new session
- Database file is created: `my_agent_database.db`
- Add some reminders or update user information

**Second Run (after closing and restarting):**
- Finds existing session automatically
- Loads previous data from database
- Continues where you left off

**Verify Persistence:**
1. Run the script and add reminders
2. Exit the program (type "exit", "quit", or "bye")
3. Run it again
4. Your reminders should still be there!

## Next Steps

Consider exploring:
- **Production Databases**: Migrating from SQLite to PostgreSQL/MySQL
- **State Migration**: Moving data between different storage backends
- **Querying History**: Using SQL to analyze conversation patterns
- **Multi-User Management**: Handling multiple users with separate sessions
- **State Cleanup**: Implementing retention policies for old sessions
- **Database Backup**: Setting up automated backups for production use
