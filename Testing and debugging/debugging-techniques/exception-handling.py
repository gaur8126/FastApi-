from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Exception)
async def general_exceptional_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'error':str(exc)}

    )


@app.get('/exception')
def handle_exceptions():
    return 1/0