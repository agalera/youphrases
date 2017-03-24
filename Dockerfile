FROM python:3.5.2-slim
MAINTAINER Alberto Galera "galerajimenez@gmail.com"
RUN echo "deb http://www.deb-multimedia.org jessie main non-free" >> /etc/apt/sources.list
RUN apt-get update -y
RUN apt-get install -y gcc
RUN apt-get install -y deb-multimedia-keyring --force-yes
RUN apt-get install -y ffmpeg --force-yes
RUN apt-get install -y sox libsox-fmt-mp3

RUN mkdir /w

WORKDIR youphrases
COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 9999
ENTRYPOINT python3 server.py
