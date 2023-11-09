#!/bin/bash

youtube-dl  -x --audio-format wav -o 'input.%(ext)s' 'https://youtu.be/K--gWoUgBNQ' 
ffmpeg -i input.wav -ss 00:04:17 -to 00:05:42 -c copy output.wav