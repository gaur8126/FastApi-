from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/wait")
async def wait():
    await asyncio.sleep(3)
    return {"message": "Finished waiting!"}