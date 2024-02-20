import logging
import soundfile
import traceback

def read_audio(file):
    logging.debug("Reading audio with soundfile: %s" % file)
    try:
        logging.debug(f"Reading audio: {file.name if hasattr(file, 'name') else file}")
        audio, sr = soundfile.read(file, dtype="float32", always_2d=True)
        logging.info(f"Read audio {file}: samplerate={sr} shape={audio.shape}")
        assert audio.shape[0] > 0, "Audio is empty"
        return audio
    except:
        logging.error("Failed to read with soundfile:\n" + traceback.format_exc())


def save_audio(file, audio, format="wav"):
    try:
        soundfile.write(file, audio.transpose(0, 1).numpy(), sr, format)
    except soundfile.LibsndfileError:
        logging.error(f"Failed to write file {file}:\n" + traceback.format_exc())
        return
    logging.info(f"Saved audio {file}: shape={audio.shape}")


def download_mode(model):
    pass
