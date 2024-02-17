FROM python:3.10-slim as build

RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    git \
    python3 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch v4.0.0 --single-branch https://github.com/facebookresearch/demucs /lib/demucs

WORKDIR /lib/demucs

RUN python3 -m pip install -e . --no-cache-dir

COPY . /app

WORKDIR /app

RUN python3 -m demucs -d cpu /app/audio-in/f8JTfLsyIHg_ffmpeg_noisy.wav

RUN rm -r separated
