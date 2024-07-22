import logging

from numpy import ndarray
from pyannote.core import Annotation
from audio.diarization.pyannote import pyannote_diarization
from audio.diarization.whisperx import whisperx_diarization

logger = logging.getLogger(__name__)


def diarization_pipeline(filename: str, diarization_method: str, save_rttm_file) -> tuple[Annotation, ndarray]:
    match diarization_method:
        case "pyannote":
            annotation, embedding = pyannote_diarization(filename, save_rttm_file)
        case "whisperx":
            annotation = whisperx_diarization(filename)
        case "nemo":
            logger.critical("Nemo not implemented. Not a valid option")

    return annotation, embedding

    # output = ""
    # rttm_annotation = read_rttm_file(filename)
    # wav_audio = load_wav_audio(construct_wav_path(filename))
    # for segment, track, label in rttm_annotation.itertracks(yield_label=True):
    #     # print(f"Speaker {label} from {segment.start:.1f}s to {segment.end:.1f}s")
    #     transcription = audio_transcribe(wav_audio, segment.start, segment.end)
    #     output += f"{label} - {transcription}\n"
    # return output
