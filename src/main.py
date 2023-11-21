from fastapi import FastAPI
import schemas
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from functions import *
from TTS.api import TTS
import random
import string
import random
import string
from TTS.api import TTS
from worker import generate_voices
from fastapi.responses import JSONResponse
from celery.result import AsyncResult

# fastapi port
server_port = 6006

app = FastAPI(docs_url=None, redoc_url=None)

app.state.tts = None

origins = ["*"]

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Set cross domain parameter transfer
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Set allowed origins sources
    allow_credentials=True,
    allow_methods=["*"],  # Set up HTTP methods that allow cross domain access, such as get, post, put, etc.
    allow_headers=["*"])  # Allowing cross domain headers can be used to identify sources and other functions.

def get_tts():
    if app.state.tts == None:
        print("Init tts")
        app.state.tts = TTS("tts_models/multilingual/multi-dataset/bark").to("cuda")
    return app.state.tts

@app.post("/tts/")
def tts_bark(item: schemas.generate_web):
    task = generate_voices.delay(item)
    return JSONResponse({"task_id": task.id})

@app.get("/tts/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)

if __name__ == '__main__':
    print_env(server_port)
    uvicorn.run(app="main:app", host="0.0.0.0", port=server_port, reload=False)