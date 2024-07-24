from audio.audio_pipeline import audio_pipeline
from database.model import Episodes
import time


# Runtime comparison for whisperx vs custom implementation
def pyannote_vs_whisperx_runtime(episode: Episodes):
    """
    Compare Pyannote diarization vs. WhiserpX diarization runtime
    Both are using whisperx for transcription
    @param episode: Episodes object to transcribe
    """
    start_time = time.time()
    transcript_pyannote = audio_pipeline(episode.filename, "pyannote", False, "whisperx", False, None)
    pyannote_imp_run_time = time.time() - start_time
    start_time = time.time()
    transcript_whisperx = audio_pipeline(episode.filename, "whisperx", False, "whisperx", False, None)
    whisperx_run_time = time.time() - start_time

    print(f"Tyler's imp: {pyannote_imp_run_time} ms\nWhisperx imp: {whisperx_run_time}")
    # Tyler's imp: 49535.377979278564 ms
    # Whisperx imp: 16695.17493247986
