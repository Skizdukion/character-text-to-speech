import random
import string
import os
from pydub import AudioSegment
import base64
import traceback

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_voices(text, char, tts):
    try:
        fname = get_random_string(6)

        file_name_wav = fname + ".wav"
        file_name_mp3 = fname + ".mp3"

        tts.tts_to_file(text=text, voice_dir=os.getcwd()+'/voices', speaker=char, file_path = os.getcwd() + "/" + file_name_wav)

        sound = AudioSegment.from_wav(file_name_wav)

        sound.export(file_name_mp3, format="mp3", bitrate="64k")

        with open(file_name_mp3, "rb") as f:
            audio_content = f.read()
        base64_audio = base64.b64encode(audio_content).decode("utf-8")

        res = {"file_base64": base64_audio,
               "audio_text": text,
               "file_name": file_name_mp3,
               }
        
        os.remove(file_name_wav)
        os.remove(file_name_mp3)
        return res
    except Exception as err:
        res = {"code": 9, "msg": "api error", "err": str(err), "traceback": traceback.format_exc()}
        return res