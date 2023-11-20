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
import random
import string
import os
from pydub import AudioSegment
import base64
import traceback
from TTS.api import TTS
from time import sleep

# fastapi port
server_port = 6006

app = FastAPI(docs_url=None, redoc_url=None)

origins = ["*"]  # set to "*" means all.

task_queue = Queue("task_queue", connection=Redis())

tts = None

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
    job_instance = task_queue.enqueue(generate_voices, item)
    while True:
        job_res = job_instance.fetch(job_instance.get_id(), connection=task_queue.connection)
        if job_res.is_finished:
            return job_res.result
        else:
            sleep(1) 


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_tts():
    global tts
    if tts == None:
        print("Starting init tts")
        tts = TTS("tts_models/multilingual/multi-dataset/bark").to("cuda") 

    return tts

def generate_voices(item: schemas.generate_web):
    print("Execute " + item.text + " at " + item.char)
    try:
        fname = get_random_string(6)

        file_name_wav = fname + ".wav"
        file_name_ogg = fname + ".ogg"

        get_tts().tts_to_file(text=item.text, voice_dir=os.getcwd()+'/voices', speaker=item.char, file_path = os.getcwd() + "/" + file_name_wav)

        sound = AudioSegment.from_wav(file_name_wav)

        sound.export(file_name_ogg, format="ogg", bitrate="64k", codec="libopus")

        with open(file_name_ogg, "rb") as f:
            audio_content = f.read()
        base64_audio = base64.b64encode(audio_content).decode("utf-8")

        res = {"file_base64": base64_audio,
               "audio_text": item.text,
               "file_name": file_name_ogg,
               }
        
        os.remove(file_name_wav)
        os.remove(file_name_ogg)
        return res
    except Exception as err:
        res = {"code": 9, "msg": "api error", "err": str(err), "traceback": traceback.format_exc()}
        print(res)
        return res

if __name__ == '__main__':
    print_env(server_port)
    uvicorn.run(app="main:app", host="0.0.0.0", port=server_port, reload=False)
