FROM ubuntu:22.04


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    build-essential \
    libgl1 \
    libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt