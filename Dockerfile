FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install espeak-ng ffmpeg -y
WORKDIR /root
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD ./src .
CMD ["python", "main.py"]