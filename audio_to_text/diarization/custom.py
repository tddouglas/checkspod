import os
import torchaudio
import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

from audio_to_text.audio_to_text import get_torch_device
from audio_to_text.transcribe.whisper_transcribe import audio_transcribe
from helpers.audio_file_helper import load_wav_audio, construct_wav_path, construct_rttm_path
from helpers.rttm_file_helper import read_rttm_file


def audio_to_text(filename, diarization_required: bool):
    """
    Custom Diarization implementation
    Take in audio file (mp4) and return text representation of it. Speakers should be tagged via diarization
    :param filename: raw filename of file to diarize
    :param diarization_required: bool to indicate if diarization is required
    :return: formatted transcript as a string
    """

    if diarization_required:
        audio_diarization(filename)

    output = ""
    rttm_annotation = read_rttm_file(filename)
    wav_audio = load_wav_audio(construct_wav_path(filename))
    for segment, track, label in rttm_annotation.itertracks(yield_label=True):
        # print(f"Speaker {label} from {segment.start:.1f}s to {segment.end:.1f}s")
        transcription = audio_transcribe(wav_audio, segment.start, segment.end)
        output += f"{label} - {transcription}\n"
    return output


# What I'm implementing - https://github.com/openai/whisper/discussions/264#discussion-4451647
# Review diarization tutorial for pyannote - https://github.com/pyannote/pyannote-audio/blob/develop/tutorials/intro.ipynb
def audio_diarization(filename: str, num_speakers=3):
    # Load pre-trained diarization pipeline - https://huggingface.co/pyannote/speaker-diarization-3.1
    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                            use_auth_token=os.getenv('HUGGING_FACE_AUTH_TOKEN'))
        pipeline.to(torch.device(get_torch_device()))
        # wav_file = construct_wav_path(filename)
        waveform, sample_rate = torchaudio.load(construct_wav_path(filename))  # preload audio to memory

        # Create terminal hooks to stay updated on model training progress
        with ProgressHook() as hook:
            diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook)
    except AttributeError as e:
        print("Error evaluating pipeline", e)

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
