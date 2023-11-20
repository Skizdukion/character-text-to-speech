from fastapi import FastAPI
import schemas
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from functions import *
from TTS.api import TTS
import random
import string
from rq import Queue
from redis import Redis
from generate_voice import generate_voices

# fastapi port
server_port = 6006

app = FastAPI(docs_url=None, redoc_url=None)

origins = ["*"]  # set to "*" means all.

tts = TTS("tts_models/multilingual/multi-dataset/bark").to("cuda") 

task_queue = Queue("task_queue", connection=Redis())

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

@app.post("/tts/")
async def tts_bark(item: schemas.generate_web):
    job_instance = task_queue.enqueue(generate_voices, item.text, item.char, tts)
    return job_instance.latest_result()

if __name__ == '__main__':
    print_env(server_port)
    uvicorn.run(app="main:app", host="0.0.0.0", port=server_port, reload=False)
