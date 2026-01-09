from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1)
    release_date: str
    director: str
    genre: str
    poster_url: str | None = None

class MovieOut(MovieCreate):
    id: int

    class Config:
        from_attributes = True
