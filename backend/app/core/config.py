import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Streamlit에서 FastAPI를 호출하려면 CORS 허용이 필요함
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")

# 감성분석 모델
SENTIMENT_MODEL_NAME = os.getenv(
    "SENTIMENT_MODEL_NAME",
    "nlp04/korean_sentiment_analysis_kcelectra"
)
