from google.adk.agents.llm_agent import LlmAgent
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import google_search

import dotenv
dotenv.load_dotenv()

# --- Constants ---
APP_NAME = "crypto_price_fetcher"
USER_ID = "dev_user_01"
SESSION_ID = "session_01"
GEMINI_MODEL = "gemini-2.0-flash"

# --- 1. Define Sub-Agents for Each Pipeline Stage ---
# Define the agent
crypto_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="crypto_price_agent",
    description="Fetches today's cryptocurrency prices and trends.",
    instruction="Use Google search to find today's cryptocurrency prices and trends. Provide a summary of the findings.",
    tools=[google_search],
    output_key="crypto_prices",
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=crypto_agent, app_name=APP_NAME, session_service=session_service)

# Agent Interaction
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            return final_response