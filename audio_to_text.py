import numpy as np
import whisper
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pyannote.core import Annotation, Timeline, Segment
import torch
from pydub import AudioSegment

from audio_file_manipulator import construct_audio_path, load_wav_audio, load_audio


# Take in audio file (mp4) and return text representation of it. Speakers should be tagged via diarization


def audio_to_text(filename, diarization_required: bool):
    if diarization_required:
        device = get_torch_device()
        audio_diarization(filename, device)

    output = ""
    rttm_annotation = read_rttm_file(filename)
    wav_audio = load_wav_audio(construct_audio_path(filename, True, 'wav'))
    for segment, track, label in rttm_annotation.itertracks(yield_label=True):
        # print(f"Speaker {label} from {segment.start:.1f}s to {segment.end:.1f}s")
        transcription = audio_transcribe(wav_audio, segment.start, segment.end)
        output += f"{label} - {transcription}\n"
    print(output)


# What I'm implementing - https://github.com/openai/whisper/discussions/264#discussion-4451647
def audio_diarization(filename: str, device: str):
    # Load pre-trained diarization pipeline - https://huggingface.co/pyannote/speaker-diarization-3.1
    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                            use_auth_token="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")
        pipeline.to(torch.device(device))
    except AttributeError as e:
        print("Error evaluating pipeline", e)

    # Create terminal hooks to stay updated on model training progress
    with ProgressHook() as hook:
        diarization = pipeline(construct_audio_path(filename, True, "wav"), num_speakers=3, hook=hook)

    # Output diarization to standard RTTM file
    with open(construct_audio_path(filename, True, "rttm"), "w") as rttm:
        diarization.write_rttm(rttm)


# Set torch device. Right now only CPU available because metal requires M2
# Add cuda support when running on Windows - torch.device("cuda")
def get_torch_device() -> str:
    print(f"PyTorch version: {torch.__version__}")

    # Check PyTorch has access to MPS (Metal Performance Shader, Apple's GPU architecture)
    print(f"Is MPS (Metal Performance Shader) built? {torch.backends.mps.is_built()}")
    print(f"Is MPS available? {torch.backends.mps.is_available()}")

    # Set the device
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    return device


def read_rttm_file(filename):
    filepath = construct_audio_path(filename, True, 'rttm')
    annotation = Annotation()
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 10:
                start_time = float(parts[3])
                duration = float(parts[4])
                end_time = start_time + duration
                speaker = parts[7]
                segment = Segment(start_time, end_time)
                annotation[segment, filename] = speaker
    return annotation


def audio_transcribe(chunked_audio: AudioSegment, audio_time_start: float, audio_time_end: float):
    trimmed_audio = chunked_audio[(audio_time_start * 1000): (audio_time_end * 1000)]  # convert seconds to MS
    np_audio = load_audio(trimmed_audio.raw_data)

    model = whisper.load_model("base.en")
    result = model.transcribe(np_audio)
    # print(f"Audio Transcribe Result:\n{result}")
    return result["text"]
