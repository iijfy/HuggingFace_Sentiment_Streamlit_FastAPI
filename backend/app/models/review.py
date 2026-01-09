from sqlalchemy import String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), index=True)

    author: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(String(2000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 감성분석 결과 저장 (프론트가 아니라 백엔드가 관리
    sentiment_label: Mapped[str] = mapped_column(String(20), nullable=False)  
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False) 

    movie = relationship("Movie", back_populates="reviews")
