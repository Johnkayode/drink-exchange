FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /drink-exchange

WORKDIR /drink-exchange

COPY . .

RUN chmod +x entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt
