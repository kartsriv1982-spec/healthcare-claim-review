from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class DecisionRequest(BaseModel):
    decision: str
    comments: str | None = None