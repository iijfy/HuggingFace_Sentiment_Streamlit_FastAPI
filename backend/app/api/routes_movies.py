from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieOut

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("", response_model=MovieOut)
def create_movie(payload: MovieCreate, db: Session = Depends(get_db)):
    movie = Movie(**payload.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

@router.get("", response_model=list[MovieOut])
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).order_by(Movie.id.desc()).all()

@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"ok": True}
