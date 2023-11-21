from TTS.api import TTS
from celery import Celery
from celery.signals import worker_process_init
from functions import *
from TTS.api import TTS
import random
import string
import os
from pydub import AudioSegment
import base64
import traceback
from TTS.api import TTS
# fastapi port

cel_app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379")
tts = None

@worker_process_init.connect()
def on_worker_init(**_):
    global tts
    tts = TTS("tts_models/multilingual/multi-dataset/bark").to("cuda")

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@cel_app.task(name='generate_voices')
def generate_voices(item):
    text = item['text']
    char = item['char']
    print("Execute " + text + " at " + char)
    try:
        fname = get_random_string(6)

        file_name_wav = fname + ".wav"
        file_name_ogg = fname + ".ogg"

        tts.tts_to_file(text=text, voice_dir=os.getcwd()+'/voices', speaker=char, file_path = os.getcwd() + "/" + file_name_wav)

        sound = AudioSegment.from_wav(file_name_wav)

        sound.export(file_name_ogg, format="ogg", bitrate="64k", codec="libopus")

        with open(file_name_ogg, "rb") as f:
            audio_content = f.read()
        base64_audio = base64.b64encode(audio_content).decode("utf-8")

        res = {"file_base64": base64_audio,
               "audio_text": char,
               "file_name": file_name_ogg,
               }
        
        os.remove(file_name_wav)
        os.remove(file_name_ogg)
        return res
    except Exception as err:
        res = {"code": 9, "msg": "api error", "err": str(err), "traceback": traceback.format_exc()}
        print(res)
        return res