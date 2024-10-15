from pydantic import BaseModel
from typing import Dict

# Data model for entering requests
class RequestData(BaseModel):
    service_type: str
    operation: str
