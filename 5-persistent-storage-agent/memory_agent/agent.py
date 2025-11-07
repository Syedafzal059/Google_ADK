from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from google.adk.tools.tool_context import ToolContext

# Load environment variables from .env file
load_dotenv()

MODEL_GPT_4O = "openai/gpt-4o"



def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a reminder to the user's list of reminders"""
    print(f"----Tool: add_reminder called for '{reminder}'")
    reminders = tool_context.session.state.get("reminders", [])
    reminders.append(reminder)
    
    # Use state_delta to ensure persistence
    tool_context.actions.state_delta = {"reminders": reminders}
    
    return{
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Reminder '{reminder}' added successfully"
    }


def view_reminders(tool_context: ToolContext) -> dict:
    """View the user's list of reminders"""
    print(f"----Tool: view_reminders called")
    reminders = tool_context.session.state.get("reminders", [])
    return{
        "action": "view_reminders",
        "reminders": reminders,
        "message": f"Reminders: {reminders}"

    }

def delete_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Delete a reminder from the user's list of reminders"""
    print(f"----Tool: delete_reminder called for '{reminder}'")
    reminders = tool_context.session.state.get("reminders", [])
    reminders.remove(reminder)
    tool_context.session.state["reminders"] = reminders
    return{
        "action": "delete_reminder",
        "reminder": reminder,
        "message": f"Reminder '{reminder}' deleted successfully"
    }

def update_reminder(reminder: str, new_reminder: str, tool_context: ToolContext) -> dict:
    """Update a reminder in the user's list of reminders"""
    print(f"----Tool: update_reminder called for '{reminder}' to '{new_reminder}'")
    reminders = tool_context.session.state.get("reminders", [])
    reminders[reminder] = new_reminder
    tool_context.session.state["reminders"] = reminders
    return{
        "action": "update_reminder",
        "reminder": reminder,
        "new_reminder": new_reminder,
        "message": f"Reminder '{reminder}' updated to '{new_reminder}' successfully"
    }

def update_user_name(user_name: str, tool_context: ToolContext) -> dict:
    """Update the user's name"""
    print(f"----Tool: update_user_name called for '{user_name}'")
    tool_context.session.state["user_name"] = user_name
    return{
        "action": "update_user_name",
        "user_name": user_name,
        "message": f"User name updated to '{user_name}' successfully"
    }




memory_agent = Agent(
    model = LiteLlm(model=MODEL_GPT_4O),
    name = 'memory_agent',
    description = 'A smart reminder agent with persistent storage',
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
    tools = [
        add_reminder,
        view_reminders,
        delete_reminder,
        update_reminder,
        update_user_name,
    ],
)

