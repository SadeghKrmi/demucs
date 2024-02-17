FROM python:3.10-slim as build
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    git \
    python3 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch v4.0.0 --single-branch https://github.com/facebookresearch/demucs /app/demucs

WORKDIR /app/demucs

RUN python3 -m pip install -e . --no-cache-dir

# COPY . /app
# WORKDIR /app
# RUN python3 -m demucs -d cpu /app/audio-in/f8JTfLsyIHg_ffmpeg_noisy.wav --out /app/audio-out/


FROM python:3.10-slim
COPY . /app
COPY --from=build /usr/local/lib/python3.10/ /usr/local/lib/python3.10/
COPY --from=build /usr/local/bin/demucs /usr/local/bin/demucs

