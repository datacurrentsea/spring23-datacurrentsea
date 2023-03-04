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
        assert response.status_code == 422
        assert response.json() == {"detail":"[422 Error] Name is not specified"}

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert "status" in response.json()
    assert datetime.fromisoformat(response.json()["status"])

def test_predict_good():
    house_data = HouseData(income=2, age=20,rooms=3,beds=1,pop=2,occupants=1,lat=32.11,long=-100.01)
    response = client.post("/predict",json=house_data.dict())
    assert response.status_code == 200

def test_predict_bad():
    #house_data = HouseData(income=2, age=20,rooms=3,beds=1,pop=2,occupants=1)
    house_data = {"income":2, "age":20,"rooms":2,"pop":1,"occupants":2,"lat":22.11,"long":-1.1}
    response = client.post("/predict",json=house_data)
    assert response.status_code == 422  
    assert response.text == '{"detail":[{"loc":["body","beds"],"msg":"field required","type":"value_error.missing"}]}' 

@pytest.mark.parametrize(
    "input_data, expected_status_code",
    [
        (
            {"income":1, "age":20,"rooms":1,"beds":2,"pop":1,"occupants":2,"lat":22.11,"long":-1.1},
            200
        ),
        (
            {"income":2, "age":30,"rooms":3,"beds":5,"pop":5,"occupants":4,"lat":2.11,"long":-10.1},
            200
        ),
        (
            {"income":3, "age":50,"rooms":5,"beds":5,"pop":9,"occupants":6,"lat":12.11,"long":-118.1},
            200,
        )
    ],
)
def test_predict_variout_input(input_data, expected_status_code):
    response = client.post("/predict",json=input_data)
    assert response.status_code == expected_status_code
