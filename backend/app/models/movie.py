from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    release_date: Mapped[str] = mapped_column(String(20), nullable=False)  # "YYYY-MM-DD" 문자열로 단순화
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=True)

    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")
