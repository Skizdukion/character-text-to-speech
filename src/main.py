from fastapi import FastAPI
import schemas
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from functions import *
from worker import generate_voices

# fastapi port
server_port = 6006

app = FastAPI(docs_url=None, redoc_url=None)

app.state.tts = None

origins = ["*"]

# Set cross domain parameter transfer
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Set allowed origins sources
    allow_credentials=True,
    allow_methods=["*"],  # Set up HTTP methods that allow cross domain access, such as get, post, put, etc.
    allow_headers=["*"])  # Allowing cross domain headers can be used to identify sources and other functions.

@app.post("/tts/")
def tts_bark(item: schemas.generate_web):
    task = generate_voices.delay({"text": item.text, "char": item.char})
    return task.get()

if __name__ == '__main__':
    print_env(server_port)
    uvicorn.run(app="main:app", host="0.0.0.0", port=server_port, reload=False)