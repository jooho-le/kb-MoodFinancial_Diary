from datetime import datetime
from pydantic import BaseModel

class ImageMeta(BaseModel):
    filename: str
    width: int
    height: int
    uploaded_at: datetime
