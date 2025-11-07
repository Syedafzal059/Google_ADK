import asyncio
from dotenv import load_dotenv
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.adk.runners import Runner
from utils import call_agent_async
from memory_agent.agent import memory_agent 
from google.genai import types
import os
from sqlalchemy import create_engine

load_dotenv()


#====== Initialize Persistent Storage ======
db_url = "sqlite:///my_agent_database.db"  
engine = create_engine(db_url)
actual_path = engine.url.database
print(f"Database will be created at: {os.path.abspath(actual_path)}")
print(f"Current working directory: {os.getcwd()}")



session_service = DatabaseSessionService(db_url=db_url)

#====== Define Initial State ======
initial_state ={
    "user_name": "Afzal",
    "reminders": [],
}

async def main_async():
    APP_NAME = "Afzal's AI Assistant"
    USER_ID = "afzal"
    

    existing_session = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    if existing_session and len(existing_session.sessions) > 0:
        SESSION_ID = existing_session.sessions[0].id  # Change: session_id -> id
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id  # Change: session_id -> id
        print(f"New session created: {SESSION_ID}")

#====== Create Runner ======
    runner = Runner(
        agent = memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Ending the conversation...Your data has been saved.")
            break

        #process the user query
        await call_agent_async(runner, user_id=USER_ID, session_id=SESSION_ID, new_message=user_input)





if __name__ == "__main__":
    asyncio.run(main_async())

