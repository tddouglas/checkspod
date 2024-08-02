import logging
from numpy import ndarray
from pyannote.core import Annotation

from audio.diarization.pyannote import pyannote_diarization
from audio.diarization.whisperx import whisperx_diarization
from database.vectordb_connector import write_embedding

logger = logging.getLogger(__name__)


def diarization_pipeline(filename: str, diarization_method: str, episode_id: str, save_rttm_file: bool) -> tuple[Annotation, ndarray]:
    match diarization_method:
        case "pyannote":
            annotation, embeddings = pyannote_diarization(filename, save_rttm_file)
            for embedding in embeddings:
                write_embedding(embedding)
        case "whisperx":
            annotation = whisperx_diarization(filename)
        case "nemo":
            logger.critical("Nemo not implemented. Not a valid option yet")

    return annotation, embedding
