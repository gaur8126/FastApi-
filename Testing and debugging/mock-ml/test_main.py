from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app 
from model import model
import numpy as np 

client = TestClient(app)


def test_predict_with_mock():
    with patch('model.model.predict') as mock_predict:
         mock_predict.return_value = [99]
         response = client.post(
              '/predict',
              json = {
                   'SepalLengthCm':5.9, 
                   'SepalWidthCm':2.3, 
                   'PetalLengthCm':1.4, 
                   'PetalWidthCm':5.1
                    
              }
         )
         assert response.status_code == 200
         assert response.json() == {'prediction':99}
        #  mock_predict.assert_called_once(np.array([[5.9, 2.3, 1.4, 5.1]]))

