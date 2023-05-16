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

class Company(BaseModel):
    Company: str

# # Identify json path
# simplawfy_object = '/app/data.json'

# # Read data object into data_json variable 
# with open(simplawfy_object) as data_object:
#     data_content = data_object.read()
#     data_json = json.loads(data_content)


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

# @app.post("/tos_summarize")
# async def generate_summary(co:Company):
#     co_tos = data_json[co]['ToS']
#     return co_tos

@app.get("/summarize")
async def stuff(company: str):
    data = {company:"Spotify's Privacy Policy is effective as of 1 January 2023. It applies to all Spotify streaming services as a user. It describes how we process your personal data at Spotify USA Inc. from now on, it will be called the Policy. It's about how Spotify processes personal data. \n\nThis Policy is not the Spotify Terms of Use, which is a separate document. It describes the rules of Spotify and your user rights. Other Spotify services include Anchor, Soundtrap, Megaphone and the Spotify Live app. Other resources and settings about your personal data are also detailed in this Policy.\n\nPrivacy Settings control processing of personal data. Notification Settings set which marketing communications you get from Spotify. On the 'Social' setting, you can start a Private session and share what you listen to on Spotify with your followers. On 'Explicit Content', you can control whether explicit-rated content can be played on your account.\n\nPrivacy laws give certain rights to individuals over their personal data. Some rights only apply when Spotify uses a certain 'legal basis' to process your data. Spotify informs you through this Policy and answers specific questions. You can edit your User Data under 'Edit profile' in your account or by contacting Spotify. Spotify is unable to delete your data in certain circumstances.\n\nThere are several ways you can delete personal data from Spotify. This data includes your User Data, Usage Data and other data listed in Section 3 'Personal data we collect about you' You can also contact us to request erasure or reach out to customer support via our chat bot. Under California law, request that Spotify limit the processing of sensitive personal data if it is used for purposes other than those specified in Section 7027 of the CCPA Regulations.\n\nYou can withdraw your consent to us collecting or using your personal data. Spotify will try to honor any request to the extent possible. You can request a copy of your data in electronic format and the right to transmit that data for use in another party's service.\n\nTailored advertising is when we use information about you to tailor ads to be more relevant to you. You can control tailored advertising in your account Privacy Settings under 'T tailored ads'. You can also control tailored ads for some podcasts using the link in the episode's show description.\n\nThe statistics about global verifiable requests we received from consumers between 1 January and 31 December 2021 show the type of request received, the average response rate and the categories of personal data we collect from you. The type of data collected and used depends on the service option you have.\n\nThis data includes profile name, email address, password, phone number, date of birth, gender, street address and university/college address. It depends on how you create your account, the country you are in, and if you use third party services to sign in.\n\nYour technical data includes: URL information, online identifiers, cookie data and IP addresses, device IDs, network connection type (e.g. wifi, 4G, LTE, Bluetooth), browser type, language, operating system, version, device name, device identifiers, brand and version, and general location.\n\nYour device sensor data is used to provide features of the Spotify Service that require this data. Voice data means audio recordings of your voice and transcripts of those recordings. Payment data includes information such as: name, date of birth, payment method, IP address, language setting and payment currency.\n\nWhen you respond to a survey or take part in user research, we collect and use the personal data you provide. If you register for or log into the Spotify Service using another service, that service sends your information to us. Third party applications, services and devices you connect to your Spotify account may also be collecting and using your data to make integration possible.\n\nSpotify collects user data from technical service partners, payment partners, merchants and acquired companies. It uses this data to provide the Spotify Service, content, and features. It also uses the data to calculate commissions owed to Spotify and understand your interests and preferences for advertising and marketing.\n\nSpotify collects limited information about your usage of the Spotify Service, including Usage Data. This is to enhance our services, products, and offerings. It is also to ensure we provide the right experience for you based on your country or region, for example based on location.\n\nIf you create a Spotify account to experience the service in full, Spotify will combine your data with your Spotify account data. The table below explains the legal justifications under data protection law for processing your personal data. You can also watch a video about Personal Data at Spotify.\n\nConsent is when Spotify asks you to indicate your agreement to Spotify's use of your personal data for a certain purpose. Compliance with legal obligations means Spotify must process your data to comply with a law. The following personal data will always be publicly available on the Spotify Service (except to any user you have blocked): your profile name, profile photo, your public playlists, who you follow and so on.\n\nThere are a few categories of data that Spotify needs to share with third parties. This includes: your profile, any content you post on Spotify and details about that content, your public playlists, third party applications, services and devices connected to your Spotify account, User Data and Usage Data.\n\nYou can share your recently played artists and playlists on your profile. You can also create or join a shared playlist with other users. Shared playlists give you social recommendations based on your listening activity. You may share your User Data to receive news or promotional offers from artists, record labels or other partners.\n\nSpotify shares user data with service providers, marketing partners, payment partners, advertising partners and hosting platforms. You have the option to change your mind and withdraw your consent at any time. Spotify does not share personal data to advertising partners by default for under-16s.\n\nSpotify shares certain data with the hosting platforms when you play a podcast. Spotify keeps your personal data only as long as necessary to provide you with the Spotify Service and for business purposes. It's your right to request that Spotify delete certain personal data. Spotify allows you to stream podcasts from other hosting platforms.\n\nSpotify keeps some data until your account is deleted and some data for a longer time period. Spotify shares personal data internationally with Spotify group companies, subcontractors and partners when carrying out the activities described in this Policy. Spotify will remove unlawful content if the law requires it to do so.\n\nTo ensure each data transfer complies with applicable EU legislation, we use the following legal mechanisms: Standard Contractual Clauses and Adequacy Decisions. We transfer personal data to vendors based in the United Kingdom, Canada, Japan, Republic of Korea and Switzerland.\n\nSpotify is committed to protecting users' personal data. To protect your account, use a strong password and limit access to your computer and browser. It's your responsibility to only allow people to use your account where you're comfortable sharing this personal data with them."}
    return data
@app.get("/tos")
async def stuff(company: str):
    data = {company:"Spotify's Privacy TOS other TOS daa. Sentence again. Formatting more text blah blah blah."}
    return data
@app.get("/qa")
async def stuff(company: str):
    data = {company:"Spotify's Privacy Question Answering other tadaa. Sentence again. Formatting more text blah blah blah."}
    return data
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