from fastapi import FastAPI, HTTPException
import uvicorn
import os
import json
import re
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def not_implemented():
    raise HTTPException(status_code=501, detail="[501 Error] Not Implemented")

@app.get("/hello")
async def hello(name: str|None = None):
    if name is not None and name != "" and name!=" ":
        return {"Hello":name}
    else:
        raise HTTPException(status_code=400, detail="[400 Error] Name is not specified")
@app.post("/predict")
async def predict(test:str|None = None):
    return {"Start": "youre not done"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
