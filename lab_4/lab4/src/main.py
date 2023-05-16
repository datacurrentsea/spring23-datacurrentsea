from fastapi import FastAPI, HTTPException
import uvicorn
import os
import json
import re
import joblib
import numpy as np
from pydantic import BaseModel, ValidationError, validator
from datetime import timezone, datetime
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

app = FastAPI()

class HouseData(BaseModel):
    income: float
    age: float
    rooms: float
    beds: float
    pop: float
    occupants: float
    lat: float
    long: float

class HousePrice(BaseModel):
    price: float

class HouseList(BaseModel):
    houses: list[HouseData]

class PriceList(BaseModel):
    prices: list[float]

###Test
class Sentiment(BaseModel):
    example: str

class SentimentRequest(BaseModel):
    text: list[Sentiment]

class SentimentResponseBase(BaseModel):
    label: str
    score: float

class SentimentResponse(BaseModel):
    predictions: list[SentimentResponseBase]


@app.post("/predict", response_model=SentimentResponse)
def predict(sentiments: SentimentRequest):
    return {"predictions": sentiments}
    # return {"predictions": classifier(sentiments.text)}

###Test

local_redis_url = "redis://redis:6379"
#local_redis_url = "redis://localhost:6379"

@app.on_event("startup")
async def startup():
    host_url = os.environ.get("redis_url", local_redis_url)
    redis = aioredis.from_url(host_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


model = joblib.load("model_pipeline.pkl")

@validator('income')
def income_positive(cls, v):
    if v < 0:
        raise ValueError('Income must be greater than 0')
    return v

@app.get("/")
async def not_implemented():
    raise HTTPException(status_code=501, detail="[501 Error] Not Implemented")

@app.get("/hello")
async def hello(name: str | None = None):
    if name is not None and name != "" and name!=" ":
        return {"Hello":name}
    else:
        raise HTTPException(status_code=422, detail="[422 Error] Name is not specified")

@app.get("/health")
async def health():
    utc_time = datetime.now(timezone.utc)
    utc_var = datetime.isoformat(utc_time)
    return {"status": utc_var}

#@cache.memoize(ttl=3600, cache_key="process_list_{input_list}")
#@cache(expire=60)
@app.post("/predict",response_model=PriceList)
@cache(expire=60)
async def predict_price(housedata: HouseList):
    data = housedata.dict()
    data_list = data['houses']
    data_vals = [list(i.values()) for i in data_list]
    data_array = np.array(data_vals)
    prices = model.predict(data_array)
    return {"prices":list(prices)}
if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True,workers=1,reload_dirs=["."])