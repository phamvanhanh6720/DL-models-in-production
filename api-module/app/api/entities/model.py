from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class DLTimeHandle(BaseModel):
    request_time: str = None
    start_inference: str = None
    end_inference: str = None


class DlResult(BaseModel):
    task_id: str
    status: str = "PENDING"
    time: dict = None
    prompt_text: str
    inference_result_uri: str = None
    error: Optional[str] = None
    
    
class DlResponse(BaseModel):
    status: str = "PENDING"
    status_code: int
    prompt_text: str
    time: datetime
    task_id: str
    