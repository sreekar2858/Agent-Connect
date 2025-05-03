import requests
import json
import dotenv
import re
import uvicorn
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from agent import call_agent

dotenv.load_dotenv()

MY_API_KEY = os.getenv("MY_API_KEY")
pushcut_api_key = os.getenv("PUSHCUT_API_KEY")
if not pushcut_api_key:
    raise HTTPException(status_code=500, detail="Pushcut API key not set in environment variables.")

def clean_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # bold
    text = re.sub(r'__([^_]+)__', r'\1', text)    # underline
    text = re.sub(r'`([^`]+)`', r'\1', text)      # inline code
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # links
    text = re.sub(r'-\s+', '', text)              # bullets
    text = re.sub(r'\n+', ' ', text)              # newlines
    return text.strip()

def send_pushcut_notification(api_key, notification_name, title, message):
    url = f"https://api.pushcut.io/{api_key}/notifications/{notification_name}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "text": message
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code

app = FastAPI()

@app.post("/agent-query")
async def agent_query(request: Request):
    # Authentication
    api_key = request.headers.get("x-api-key")
    if api_key != MY_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Get and validate query
    data = await request.json()
    user_query = data.get("message", "").strip()

    if not user_query:
        raise HTTPException(status_code=400, detail="Empty query")

    # Process with agent
    try:
        print(f"Processing query: {user_query}")
        agent_response = call_agent(user_query)
        cleaned_response = clean_text(agent_response)
    except Exception as e:
        print(f"Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail="Agent processing failed")

    # Send push notification
    notification_name = "JobAgent"
    title = "Crypto Prices Update"
    message = cleaned_response
    status = send_pushcut_notification(pushcut_api_key, notification_name, title, message)
    if status == 200:
        print("Push notification sent successfully.")
    else:
        print(f"Failed to send push notification. Status code: {status}")

    return JSONResponse(content={
        "status": "success",
        "original_query": user_query,
        "agent_response": cleaned_response
    })

@app.post("/run-agent")
async def run_agent(request: Request):
    # API Key Authentication
    api_key = request.headers.get("x-api-key")
    if api_key != MY_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    print("Starting cryptocurrency price fetch...")
    result = call_agent("Summarize today's cryptocurrency prices and trends in 4-5 simple spoken sentences, suitable for Siri to read aloud.")
    result = clean_text(result)
    
    # Send push notification
    notification_name = "JobAgent"
    title = "Crypto Prices Update"
    message = result
    status = send_pushcut_notification(pushcut_api_key, notification_name, title, message)
    if status == 200:
        print("Push notification sent successfully.")
    else:
        print(f"Failed to send push notification. Status code: {status}")

    return JSONResponse(content={
        "status": "success",
        "message": "Agent executed successfully.",
        "agent_response": result
    })

if __name__ == "__main__":
    filename = os.path.splitext(os.path.basename(__file__))[0]
    uvicorn.run(f"{filename}:app", host="0.0.0.0", port=8765, reload=True)
