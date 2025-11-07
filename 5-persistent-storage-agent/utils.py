from google.genai import types


async def call_agent_async(runner, user_id, session_id, new_message):
    """call the agent asynchronously with users query"""
    content = types.Content(
        role="user",
        parts=[types.Part(text=new_message)],
    )
    print(f"Processing user query: {new_message}")

    final_response = None

    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State BEFORE processing user query"
    )

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            response = await process_agent_response(event)
            if response:
                final_response = response
    except Exception as e:
        print(f"Error processing user query: {e}")


async def process_agent_response(event):
    """process the agent response"""
    if event.is_final_response:
        if event.content and event.content.parts:
            return event.content.parts[0].text
    return None


async def display_state(session_service, app_name, user_id, session_id, message):
    """display the state of the session"""
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    print(f"\n{message}\n")
    for key, value in session.state.items():
        print(f"{key}: {value}")