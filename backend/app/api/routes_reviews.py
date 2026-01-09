from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.review import Review
from app.models.movie import Movie
from app.schemas.review import ReviewCreate, ReviewOut
from app.core.sentiment import predict_sentiment

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("", response_model=ReviewOut)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == payload.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    s = predict_sentiment(payload.content)

    review = Review(
        movie_id=payload.movie_id,
        author=payload.author,
        content=payload.content,
        sentiment_label=s["label"],
        sentiment_score=s["score"],
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("", response_model=list[ReviewOut])
def list_reviews(
    movie_id: int | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Review)
    if movie_id is not None:
        q = q.filter(Review.movie_id == movie_id)
    return q.order_by(Review.created_at.desc()).limit(limit).all()

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"ok": True}

@router.get("/ratings/{movie_id}")
def get_movie_rating(movie_id: int, db: Session = Depends(get_db)):
    
    rows = db.query(Review.sentiment_label, Review.sentiment_score).filter(Review.movie_id == movie_id).all()
    if not rows:
        return {"movie_id": movie_id, "rating": None, "count": 0}

    total = 0.0
    for label, score in rows:
        total += score if label == "POS" else -score if label == "NEG" else 0.0

    return {"movie_id": movie_id, "rating": total / len(rows), "count": len(rows)}
