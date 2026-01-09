from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.core.config import CORS_ALLOW_ORIGINS
from app.api.routes_movies import router as movies_router
from app.api.routes_reviews import router as reviews_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Reviews API",
    description="영화 등록/조회/삭제, 리뷰 등록/조회/삭제, 리뷰 감성분석 및 평점(감성 평균) 제공",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies_router)
app.include_router(reviews_router)

@app.get("/")
def health():
    return {"ok": True}
