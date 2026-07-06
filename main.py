from fastapi import FastAPI
from models import AgentRequest
from agent.core import run_agent
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = FastAPI(title="System Design AI Agent")

@app.get("/")
def home():
    return {
        "status":"running",
        "message":"Agent is ready"
    }
@app.post("/agent")
def agent_endpoint(req: AgentRequest):
    result = run_agent(req.request)
    return result
