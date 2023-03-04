from fastapi import FastAPI, HTTPException
import uvicorn
import os
import json
import re
import joblib
import numpy as np
from pydantic import BaseModel, ValidationError, validator
from datetime import timezone, datetime

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


@app.post("/predict",response_model=PriceList)
#@app.post("/predict")
async def predict_price(housedata: HouseList):
    data = housedata.dict()
    data_list = data['houses']
    data_vals = [list(i.values()) for i in data_list]
    data_array = np.array(data_vals)
    print(np.shape(data_array))
    prices = model.predict(data_array)
    print(prices)
    return {"prices":list(prices)}
if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True,workers=1,reload_dirs=["."])