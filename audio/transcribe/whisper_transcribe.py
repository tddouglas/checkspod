import logging
import whisper
from pydub import AudioSegment
from helpers.audio_file_helper import load_audio

logger = logging.getLogger(__name__)


def audio_transcribe(chunked_audio: AudioSegment, audio_time_start: float, audio_time_end: float):
    trimmed_audio = chunked_audio[(audio_time_start * 1000): (audio_time_end * 1000)]  # convert seconds to MS
    np_audio = load_audio(trimmed_audio.raw_data)

    model = whisper.load_model("base.en")
    result = model.transcribe(np_audio)
    logger.debug(f"Audio Transcribe Result:\n{result}")
    return result["text"]
