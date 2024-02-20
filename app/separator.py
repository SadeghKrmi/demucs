import os
import glob
from pathlib import Path
import demucs.api as deap
import typing as tp
import audio
import logging


repo = Path("/app/models/")
audio_file_wav = "/app/audio-in/f8JTfLsyIHg_ffmpeg_noisy.wav"
audio_file_mp3 = "/app/audio-in/audio_example.mp3"


class Separator:
    def __init__(self, repo: tp.Optional[tp.Callable[[str], None]], model: str = "htdemucs"):
        self.separator = deap.Separator(model=model, progress=False)
        self.model = model
        
    def separate(self, file):
        filename = os.path.basename(file)
        logging.info("Start separating audio: %s" % filename)
        origin, separated = self.separator.separate_audio_file(file)



    # def download_model(self, model):
    #     remote_urls = {}
    #     new_models = deap.list_models()["bag"]
    #     for sig, filepath in new_models.items():
    #         remote_urls[sig] = str(filepath)
            
    #     if isinstance(remote_urls[model], list):
    #         pass
        # if model in self.downloaded_models:
        #     req = urllib.request.Request(url, headers={"User-Agent": "torch.hub"})
        #     u = urllib.request.urlopen(req)
        #     return
        
        

sep = Separator(model="htdemucs", repo =None)
origin, separated = sep.separate(audio_file_wav)