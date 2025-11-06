from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from uuid import uuid4
from question_answering_agent.agent import question_answering_agent 
load_dotenv()
from google.genai import types

session_service_stateful = InMemorySessionService()

initial_state ={
    "user_name": "Afzal",
    "user_preferences": """
        I like cricket and I like to play cricket.
        I am an Agentic AI Developer
        I am from India"""
}


APP_NAME = "Afzal's AI Assistant"
USER_ID = "afzal"
SESSION_ID = str(uuid4())
stateful_session = session_service_stateful.create_session_sync(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)

print("Stateful session created successfully")
print(f"\nSession ID: {SESSION_ID}")


runner = Runner(
    agent = question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

new_message = types.Content(
    role="user", parts=[types.Part(text="What is Afzal's favorite sport?")])

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response:
        if event.content and event.content.parts:
            print(f"Final response: {event.content.parts[0].text}")


print("======Session Event Exploration======\n")
session = session_service_stateful.get_session_sync(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

print("===Final Session State===\n")
for key, value in session.state.items():
    print(f"{key}: {value}")