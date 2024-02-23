FROM python:3.11-slim
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    git \
    python3 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone --depth 1 --branch v4.0.1 --single-branch https://github.com/facebookresearch/demucs /app/demucs

# API developement
RUN git clone --depth 1 --single-branch https://github.com/facebookresearch/demucs /app/demucs

WORKDIR /app/demucs

RUN python3 -m pip install . --no-cache-dir

COPY . /app

WORKDIR /app

RUN python3 -m demucs -d cpu /app/audio-in/f8JTfLsyIHg_ffmpeg_noisy_quarter.wav --two-stems=vocals --out /app/audio-out/
