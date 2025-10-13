FROM python:3.12 AS base

RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh