from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import schemas
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from functions import *
import base64
import os
import traceback
from TTS.api import TTS
from bark import SAMPLE_RATE

import soundfile as sf
import wave
import numpy as np
import nltk
import torch
import random
import string
import subprocess

# fastapi port
server_port = 6006

app = FastAPI(docs_url=None, redoc_url=None)

origins = ["*"]  # set to "*" means all.

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/bark").to(device)

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
    time_start = time.time()
    try:
        fname = get_random_string(6)

        file_name_wav = fname + ".wav"
        file_name_ogg = fname + ".ogg"

        tts.tts_to_file(text=item.text, voice_dir=os.getcwd()+'/src/voices', speaker=item.char, file_path = os.getcwd() + file_name_wav)

        # convert to OGG
        subprocess.run(["ffmpeg", "-i", file_name_wav, "-c:a", "libopus", "-b:a", "64k", "-y", file_name_ogg], check=True)

        with open(file_name_ogg, "rb") as f:
            audio_content = f.read()
        base64_audio = base64.b64encode(audio_content).decode("utf-8")

        res = {"file_base64": base64_audio,
               "audio_text": item.text,
               "file_name": file_name_ogg,
               }
        
        print_log(item, res, time_start)
        os.remove(file_name_wav)
        os.remove(file_name_ogg)
        return res
    except Exception as err:
        res = {"code": 9, "msg": "api error", "err": str(err), "traceback": traceback.format_exc()}
        print_log(item, res, time_start)
        return res

if __name__ == '__main__':
    print_env(server_port)
    uvicorn.run(app="main:app", host="0.0.0.0", port=server_port, reload=False)
