import logging

from audio.diarization.pipeline import diarization_pipeline
from helpers.rttm_file_helper import read_rttm_file
from helpers.txt_file_helper import write_to_text_file

logger = logging.getLogger(__name__)


def audio_pipeline(filename: str, diarization_method:str, save_rttm_file: bool, transcribe_method: str, save_transcript: bool, verification_pipeline: str):
    if diarization_method:
        annotation = diarization_pipeline(filename, diarization_method, save_rttm_file)
    else:  # Diarization should already exist in RTTM file
        annotation = read_rttm_file(filename)

    if transcribe_method:
        transcript = "To Implement"
        if save_transcript:
            write_to_text_file(filename, transcript)