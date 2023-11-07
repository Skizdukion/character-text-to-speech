import os
import subprocess

if not os.path.exists('bark'):
    subprocess.run(['git', 'clone', 'https://huggingface.co/suno/bark'])
    subprocess.run(['cd', 'bark'])
    subprocess.run(['rm', '-rf', 'speaker-embeddings'])
    subprocess.run(['rm', 'coarse.pt'])
    subprocess.run(['rm', 'fine.pt'])
    subprocess.run(['rm', 'text.pt'])
    subprocess.run(['git', 'lfs', 'pull'])
