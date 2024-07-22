import os
import torchaudio
import torch
from numpy import ndarray
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pyannote.core import Annotation

from audio.torch import get_torch_device
from helpers.audio_file_helper import construct_wav_path, construct_rttm_path


# What I'm implementing - https://github.com/openai/whisper/discussions/264#discussion-4451647
# Review diarization tutorial for pyannote - https://github.com/pyannote/pyannote-audio/blob/develop/tutorials/intro.ipynb
def pyannote_diarization(filename: str, save_rttm_file, num_speakers=3) -> tuple[Annotation, ndarray]:
    # Load pre-trained diarization pipeline - https://huggingface.co/pyannote/speaker-diarization-3.1
    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                            use_auth_token=os.getenv('HUGGING_FACE_AUTH_TOKEN'))
        pipeline.to(torch.device(get_torch_device()))
        # wav_file = construct_wav_path(filename)
        waveform, sample_rate = torchaudio.load(construct_wav_path(filename))  # preload audio to memory

        with ProgressHook() as hook:
            diarization, embeddings = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook,
                                               num_speakers=num_speakers, return_embeddings=True)
    except AttributeError as e:
        print("Error evaluating pipeline", e)

    if save_rttm_file:
        # Output diarization to standard RTTM file
        try:
            with open(construct_rttm_path(filename), "w") as rttm:
                diarization.write_rttm(rttm)
        except IOError as e:
            # Handles exceptions raised by file operations (e.g., file not found, disk full, etc.)
            print(f"An error occurred while writing the file: {e}")
        except Exception as e:
            # This is a more general exception to catch any other exceptions that may occur
            print(f"An unexpected error occurred: {e}")

    return diarization, embeddings
