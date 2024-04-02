import os
import whisperx
import gc
import torchaudio
import whisper
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pyannote.core import Annotation, Timeline, Segment
import torch
from pydub import AudioSegment
from audio_file_manipulator import load_wav_audio, load_audio, construct_wav_path, construct_rttm_path


# Take in audio file (mp4) and return text representation of it. Speakers should be tagged via diarization


def audio_to_text(filename, diarization_required: bool):
    if diarization_required:
        audio_diarization(filename)

    output = ""
    rttm_annotation = read_rttm_file(filename)
    wav_audio = load_wav_audio(construct_wav_path(filename))
    for segment, track, label in rttm_annotation.itertracks(yield_label=True):
        # print(f"Speaker {label} from {segment.start:.1f}s to {segment.end:.1f}s")
        transcription = audio_transcribe(wav_audio, segment.start, segment.end)
        output += f"{label} - {transcription}\n"
    print(output)


# What I'm implementing - https://github.com/openai/whisper/discussions/264#discussion-4451647
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


# Set torch device
def get_torch_device() -> str:
    print(f"PyTorch version: {torch.__version__}")

    # Set the device
    if torch.cuda.is_available():
        device = 'cuda'
    elif torch.backends.mps.is_available():
        device = 'mps'
    else:
        device = 'cpu'
    print(f"Using device: {device}")
    return device


def read_rttm_file(filename):
    filepath = construct_rttm_path(filename)
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


# Utilizes Whipserx for diarlization and transcription instead of Custom Implementation above.
def whisperx_diarization_transcribe(filename) -> str:
    audio_file = construct_wav_path(filename)
    device = get_torch_device()
    batch_size = 16  # reduce if low on GPU mem
    compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)
    options = {
        "max_new_tokens": None,
        "clip_timestamps": None,
        "hallucination_silence_threshold": None,
    }

    model = whisperx.load_model("large-v2", device, compute_type=compute_type,asr_options=options)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    print("Before Alignment\n", result["segments"])  # before alignment

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    print("After Alignment\n", result["segments"])  # after alignment


    # 3. Assign speaker labels
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=os.getenv('HUGGING_FACE_AUTH_TOKEN'), device=device)

    # add min/max number of speakers if known
    diarize_segments = diarize_model(audio)
    # diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

    result = whisperx.assign_word_speakers(diarize_segments, result)
    final_res = ""
    for segment in result["segments"]:
        formatted_text = f"{segment['speaker']} - {segment['text']}"
        final_res += formatted_text + '\n'

    print(f"Final text is:\n{final_res}")
    return final_res