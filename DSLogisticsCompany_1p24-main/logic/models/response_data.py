from pydantic import BaseModel
from typing import Dict

# Data model for responses
class ResponseData(BaseModel):
    status_code: int
    response: dict