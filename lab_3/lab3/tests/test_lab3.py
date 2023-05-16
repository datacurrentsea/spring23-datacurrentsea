import pytest
from fastapi.testclient import TestClient 
from unittest import mock
import httpx 
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()
from src.main import *

client = TestClient(app)

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
    raw_output = response.json()
    output = raw_output["prices"]
    assert response.status_code == 200
    assert isinstance(output,list)
    for value in output:
        assert isinstance(value,float)

def test_predict_bad_type():
    house_data = {"houses":[{"income": 1, "age": 20, "rooms": 3, "beds": 2,"pop":20,"occupants":"four","lat":32.11,"long":11.1},{"income": 1, "age": 20, "rooms": 3, "beds": 2,"pop":"twenty20","occupants":"four","lat":32.11,"long":-10.1}]}
    response = client.post("/predict",json=house_data)
    assert response.status_code == 422  
    raw_output = response.json()
    output = raw_output["detail"]
    for i in output:
        assert i["msg"] == "value is not a valid float"
        assert i["type"] == "type_error.float"

def test_predict_missing_val():
    house_data = {"houses":[{"income": 1, "age": 30, "rooms": 2, "beds": 1,"pop":10,"occupants":2},{"rooms": 2, "beds": 1,"pop":10,"occupants":2},{"income": 1}]}
    response = client.post("/predict",json=house_data)
    assert response.status_code == 422  
    raw_output = response.json()
    output = raw_output["detail"]
    for i in output:
        assert i["msg"] == "field required"
        assert i["type"] == "value_error.missing"