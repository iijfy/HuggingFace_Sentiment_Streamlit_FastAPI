from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

# safetensors 제공되는 한국어 감성분석 모델
MODEL_NAME = "Copycats/koelectra-base-v3-generalized-sentiment-analysis"

_pipeline = None

def get_pipeline():
   
    global _pipeline
    if _pipeline is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            use_safetensors=True,  
        )
        _pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)
    return _pipeline

def predict_sentiment(text: str) -> dict:
 
    pipe = get_pipeline()
    pred = pipe(text)[0] 

    label_raw = str(pred["label"])
    score = float(pred["score"])

    label = "POSITIVE" if label_raw == "1" else "NEGATIVE"
    return {"label": label, "score": score}
