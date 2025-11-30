from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import redis
import hashlib
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] (line %(lineno)d) - %(levelname)s - %(message)s",
    datefmt="%m-%d-%Y %H:%M:%S"
)

logging.info("FastAPI instence created")
app = FastAPI()

logging.info("redis client initiated")
redis_client = redis.Redis(host='localhost',port=6379,db=0)

logging.info("ml model loaded")
model = joblib.load("model.joblib")


class IrisFlower(BaseModel):
    SepalLengthCm:float
    SepalWidthCm:float
    PetalLengthCm:float
    PetalWidthCm:float

    def to_list(self):
        """Return the values as a list"""
        logging.info("Inside the to_list function")
        return [
            self.SepalLengthCm,
            self.SepalWidthCm,
            self.PetalLengthCm,
            self.PetalWidthCm
        ]
    
    def cache_key(self):
        """Returns Unique identifier of sorts"""
        logging.info("Inside the cache_key function")
        raw = json.dumps(self.model_dump(), sort_keys=True)
        return f"Predict: {hashlib.sha256(raw.encode()).hexdigest()}"
    

logging.info("predict endpoint.......")
@app.post('/predict')
async def predict(data:IrisFlower):
    key = data.cache_key()


    cached_result = redis_client.get(key)
    if cached_result:
        print("Serving prediction from Cache!")
        return json.loads(cached_result)
    
    prediction = model.predict([data.to_list()])[0]
    result = {'prediction': int(prediction)}
    redis_client.set(key,json.dumps(result), ex=3600)
    logging.info(f"Predicted result: {result}")
    return result

