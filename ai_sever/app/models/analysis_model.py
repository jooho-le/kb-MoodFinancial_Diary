from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalysisData(BaseModel):
    user_id: Optional[str]
    emotion: str
    category: str
    amount: float
    timestamp: datetime
    description: Optional[str] = None
