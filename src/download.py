import os

url = ''

parts = []

idx = 0

output_parts = []

os.system("youtube-dl  -x --audio-format wav -o 'input.%(ext)s' " + url)

for part in parts:
    os.system("ffmpeg -i input.wav -ss " + part[0] + " -to " + part[1] + " -c copy " + str(idx) + ".wav")
    output_parts.append(str(idx) + ".wav")
    idx += 1

with open('list.txt', 'w') as f:
    for wav_file in output_parts:
        f.write(f"file '{wav_file}'\n")

os.system("ffmpeg -f concat -safe 0 -i list.txt -c copy output.wav")

for wav_file in output_parts:
        os.remove(wav_file)

os.remove('list.txt')
os.remove('input.wav')