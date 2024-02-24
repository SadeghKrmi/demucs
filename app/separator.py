import os
import sys
import torch
from pathlib import Path
import demucs.api as deapi
import demucs.apply as deapply
import typing as tp
import audio as ao
import logging
import time

DEFAULT_REPO = "/app/models/"
DEFAULT_AUDIO_OUT = "/app/audio-out/"
DEFAULT_MODEL = "htdemucs"


"""
# python separator.py --input /app/audio-in/f8JTfLsyIHg_ffmpeg_noisy_quarter.wav --model htdemucs
"""


def parse_arguments(args):
    parsed_args = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            key = args[i][2:]
            value = args[i + 1]
            parsed_args[key] = value
            i += 2
        elif args[i].startswith("-") and i + 1 < len(args):
            key = args[i][1:]
            value = args[i + 1]
            parsed_args[key] = value
            i += 2
        else:
            # print(f"Ignoring argument: {args[i]}")
            parsed_args["_input"] = value
            i += 1
    return parsed_args


class Separator:
    def __init__(self, repo: tp.Optional[tp.Callable[[str], None]], model: str = "htdemucs"):
        self.separator = deapi.Separator(model=model, repo=repo, progress=False)
        self.model = model
        self.repo = repo
        
        if not isinstance(self.separator.model, deapply.BagOfModels):
            self.default_segment = self.separator.model.segment
        else:
            self.default_segment = min(i.segment for i in self.separator.model.models)  # type: ignore
            if hasattr(self.separator.model, "segment"):
                self.default_segment = min(self.default_segment, self.separator.model.segment)
        self.default_segment = max(self.default_segment, 0.1)
        self.sources = self.separator.model.sources
        
    def separate_from_audio(self, audio_file):
        wav, sampling_rate_of_audio = ao.read_audio(audio_file)
        self.filename = os.path.basename(audio_file)
        self.filepath = os.path.abspath(audio_file)
        self.output_path = "/app/audio-out/" + self.filename.split(".")[0]
        self.time_hists = []
        
        logging.info(f"Start separating {self.filename} audio")
        
        wav_torch = torch.from_numpy(wav).clone().transpose(0, 1)
        src_channels = wav_torch.shape[0]
        logging.info("Running separation...")
        self.time_hists.append((time.time(), 0))
        if src_channels != self.separator.model.audio_channels:
            out = {stem: torch.zeros(1, wav_torch.shape[1], dtype=torch.float32) for stem in self.sources}
            self.in_length = src_channels
            self.out_length = 0
            for i in range(src_channels):
                self.out_length += 1
                for stem, tensor in self.separator.separate_tensor(
                    wav_torch[i, :].repeat(self.separator.model.audio_channels, 1)
                )[1].items():
                    out[stem][i, :] = tensor.sum(dim=0) / tensor.shape[0]
        else:
            self.in_length = 1
            self.out_length = 0
            out = self.separator.separate_tensor(wav_torch)[1]
        ao.save_audio(self.output_path, out, sr=sampling_rate_of_audio)
        return


if __name__ == "__main__":
    options = parse_arguments(sys.argv)
    # repo = Path(options.get('repo', DEFAULT_REPO))
    model = options.get('model', DEFAULT_MODEL)
    audio_input = options.get('input', None)
    
    sep = Separator(model=model, repo=None)
    sep.separate_from_audio(audio_input)
