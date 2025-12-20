FROM python:3.10.9 AS base

RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt