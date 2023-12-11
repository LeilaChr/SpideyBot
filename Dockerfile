FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt update && \
	apt install -y python3-pip

WORKDIR /app

COPY src/* src/

COPY requirements.txt .

COPY .env .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
