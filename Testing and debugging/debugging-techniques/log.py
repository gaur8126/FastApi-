import logging
from fastapi import FastAPI

app = FastAPI()

logging.basicConfig(
    level= logging.INFO,
    format="[%(asctime)s] (line %(lineno)d) - %(levelname)s - %(message)s",
    datefmt="%m-%d-%Y %H:%M:%S"
)

@app.get('/debug')
def debug_route():
    logging.info("API Endpoint hit.")
    return {'message': 'Check logs!'}