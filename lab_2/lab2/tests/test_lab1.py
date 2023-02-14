import pytest
from fastapi.testclient import TestClient 
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
        assert response.status_code == 400
        assert response.json() == {"detail":"[400 Error] Name is not specified"}