import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api import api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/")
def default():
    return JSONResponse(content={"response": "ok"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
