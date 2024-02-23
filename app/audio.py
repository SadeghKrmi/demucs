import os
import soxr
import logging
import soundfile
import traceback

def read_audio(file, target_sr=None):
    logging.debug("Reading audio with soundfile: %s" % file)
    try:
        logging.debug(f"Reading audio: {file.name if hasattr(file, 'name') else file}")
        audio, sr = soundfile.read(file, dtype="float32", always_2d=True)
        logging.info(f"Read audio {file}: samplerate={sr} shape={audio.shape}")
        assert audio.shape[0] > 0, "Audio is empty"
        if target_sr is not None and sr != target_sr:
            logging.info(f"Samplerate {sr} doesn't match target {target_sr}, resampling with SoXR")
            audio = soxr.resample(audio, sr, target_sr, "VHQ")
            sr = target_sr
        return audio, sr
    except:
        logging.error("Failed to read with soundfile:\n" + traceback.format_exc())


def save_audio(path, audio, sr, format="PCM_24"):
    try:
        os.makedirs(path)
        for stem, source in audio.items():
            file = path + "/" + stem + ".wav"
            soundfile.write(file, source.transpose(0, 1).numpy(), sr, format)
    except soundfile.LibsndfileError:
        logging.error(f"Failed to write to the output {path}:\n" + traceback.format_exc())
        return
