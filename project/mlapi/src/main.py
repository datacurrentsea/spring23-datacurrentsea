import logging
import os
from fastapi import FastAPI, Request, Response
import uvicorn
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    return_all_scores=True,
)

logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://redis:6379"
app = FastAPI()


@app.on_event("startup")
def startup():
    host_url = os.environ.get("redis_url", LOCAL_REDIS_URL)
    redis = aioredis.from_url(host_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# class Sentiment(BaseModel):
#     example: str

class SentimentRequest(BaseModel):
    text: list[str]

class SentimentResponseBase(BaseModel):
    label: str
    score: float

class SentimentResponse(BaseModel):
    predictions: list[list[SentimentResponseBase]]


@app.post("/predict", response_model=SentimentResponse)
def predict(sentiments: SentimentRequest):
    return {"predictions": classifier(sentiments.text)}


@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    #uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True,workers=1,reload_dirs=["."])