FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update

RUN apt install ffmpeg=7:4.4.2-0ubuntu0.22.04.1 -y

WORKDIR /root

ADD ./requirements.txt .
RUN pip install --ignore-installed blinker==1.7.0
RUN pip install -r requirements.txt
ADD ./src .

RUN apt install redis -y
RUN touch worker.log
CMD bash -c "redis-server & celery -A worker worker --loglevel=info --concurrency=1 -f worker.log & python main.py"