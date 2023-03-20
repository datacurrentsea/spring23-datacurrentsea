import pytest
from fastapi.testclient import TestClient 
from unittest import mock
import httpx 

# def mock_cache(*args, **kwargs):
#     def wrapper(func):
#         @wraps(func)
#         async def inner(*args, **kwargs):
#             return await func(*args, **kwargs)
#         return inner
#     return wrapper

# mock.patch("fastapi_cache.decorator.cache", mock_cache).start()    

# @pytest.fixture(scope="module")
# async def client():
#     from src.main import app # need to load app module after mock. otherwise, it would fail
#     async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
#         yield client
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
from src.main import *
client = TestClient(app)
#client = client(app)
def test_root():
    response = client.get("/")
    assert response.status_code == 501
    assert response.json() == {"detail": "[501 Error] Not Implemented"}

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_api():
    valid_version = 3.0
    response = client.get("/openapi.json")
    json_response = response.json()
    assert response.status_code == 200
    assert float((re.match('\d\.\d',json_response['openapi']).group(0))) >= valid_version

def test_hello():
    hello_examples = ['prof','Gigi','Eleven']
    for i in hello_examples:
        test_endpoint = "hello?name="+i
        response = client.get(test_endpoint)
        assert response.status_code == 200
        assert response.json() == {"Hello": i}

def test_hello_no_name():
    hello_bad_examples = ['name=','',' ','name= ']
    for i in hello_bad_examples:
        test_endpoint = "hello?"+i
        print(test_endpoint)
        response = client.get(test_endpoint)
        assert response.status_code == 422
        assert response.json() == {"detail":"[422 Error] Name is not specified"}

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert "status" in response.json()
    assert datetime.fromisoformat(response.json()["status"])

def test_predict_good():
    house_data = {"houses":[{"income": 1, "age": 20, "rooms": 3, "beds": 2,"pop":20,"occupants":4,"lat":32.11,"long":11.1},{"income": 1, "age": 30, "rooms": 2, "beds": 1,"pop":10,"occupants":2,"lat":1.1,"long":2.1}]}
    response = client.post("/predict",json=house_data)
    #response = client.post("/predict",json=house_data)
    assert response.status_code == 200

# def test_predict_bad():
#     house_data = {"houses":[{"income": 1, "age": 20, "rooms": 3, "beds": 2,"pop":20,"occupants":"four","lat":32.11,"long":11.1},{"income": 1, "age": 30, "rooms": 2, "beds": 1,"pop":10,"occupants":2}]}
#     response = client.post("/predict",json=house_data)
#     assert response.status_code == 422  
#     #assert response.text == '{"detail":[{"loc":["body","beds"],"msg":"field required","type":"value_error.missing"}]}' 