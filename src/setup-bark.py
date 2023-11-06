import os
import subprocess

if not os.path.exists('bark'):
    subprocess.run(['git', 'clone', 'https://huggingface.co/suno/bark'])