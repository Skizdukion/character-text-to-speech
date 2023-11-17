FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update

RUN apt install espeak-ng wget unzip ffmpeg -y

WORKDIR /root

RUN wget https://github.com/Skizdukion/character-text-to-speech/raw/main/voices.zip

RUN unzip voices.zip && rm voices.zip

ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD ./src .

RUN mv src/voices/ .
RUN rm -rf src

CMD ["python", "main.py"]