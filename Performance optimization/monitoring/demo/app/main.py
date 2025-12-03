from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)


@app.get('/')
def root():
    return {'message':'Fast API with Prometheus and Docker!'}

