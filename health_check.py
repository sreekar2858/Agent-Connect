from fastapi import FastAPI, Request
from flask import app
from agent import *

@app.post("/run_agent")
async def run_agent(request: Request):
    data = await request.json()
    query = data.get("query")
    result = call_agent(query)
    # Pushcut notification here if needed
    return {"result": result}
