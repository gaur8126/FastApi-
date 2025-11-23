from fastapi import FastAPI
from schema import InputSchema, OutputSchema
from predict import make_prediction, make_batch_prediciton
from typing import List


app =FastAPI()

@app.get("/")
def index():
    return {"message":"Welcome to the prediction api"}


@app.post("/prediction",response_model=OutputSchema)
def predict(user_input: InputSchema):
    prediction = make_prediction(user_input.model_dump())
    return OutputSchema(predicted_price= round(prediction, 2))

@app.post('/batch_prediction', response_model=List[OutputSchema])
def batch_predict(user_inputs:List[InputSchema]): 
    predictions = make_batch_prediciton([x.model_dump() for x in user_inputs]) 
    return [OutputSchema(predicted_price=round(predict,2)) for predict in predictions]

