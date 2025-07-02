from pydantic import BaseModel
from typing import List

class PlanRequest(BaseModel):
    destination: str
    days: int
    interests: List[str]
