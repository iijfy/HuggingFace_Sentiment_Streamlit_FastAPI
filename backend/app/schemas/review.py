from pydantic import BaseModel, Field
from datetime import datetime

class ReviewCreate(BaseModel):
    movie_id: int
    author: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

class ReviewOut(BaseModel):
    id: int
    movie_id: int
    author: str
    content: str
    created_at: datetime
    sentiment_label: str
    sentiment_score: float

    class Config:
        from_attributes = True
