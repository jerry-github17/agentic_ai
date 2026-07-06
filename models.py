from pydantic import BaseModel
class AgentRequest(BaseModel):
    request: str


class AgentResponse(BaseModel):
    status:str
    execution_plan: list[str]
    document_path: str
    message: str