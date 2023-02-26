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

class HouseList(BaseModel):
    data: list[HouseData]

class HousePrice(BaseModel):
    price: float


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


@app.post("/predict",response_model=HousePrice)
async def predict_price(housedata: HouseData):
    house_dict = housedata.dict()
    house_vals = list(house_dict.values())
    house_vector = np.array(house_vals)
    house_price = model.predict(house_vector.reshape(-1,8))
    return {"price":house_price[0]}

if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True,workers=1,reload_dirs=["."])