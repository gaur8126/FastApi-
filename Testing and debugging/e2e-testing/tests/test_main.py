from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)


def test_eligibility_pass():
    response = client.post(
        '/loan-eligibility',
        json = {
            'income':60000,
            'age':30,
            'employment_status':'employed'
        }
    )

    assert response.status_code == 200
    assert response.json() == {'eligible':True}


    
def test_eligibility_fail():
    response = client.post(
        '/loan-eligibility',
        json = {
            'income':20000,
            'age':19,
            'employment_status':'unemployed'
        }
    )

    assert response.status_code == 200
    assert response.json() == {'eligible':False}


