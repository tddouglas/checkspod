from database.model import Episodes
import time
from audio_to_text.diarization.custom import audio_to_text
from audio_to_text.diarization.whisperx import whisperx_diarization_transcribe


# Runtime comparison for whisperx vs custom implementation
def custom_vs_whisperx_runtime(episode: Episodes):
    start_time = time.time()
    transcript_custom = audio_to_text(episode.filename, True)
    custom_imp_run_time = time.time() - start_time
    start_time = time.time()
    transcript_whisperx = whisperx_diarization_transcribe(episode.filename)
    whisperx_run_time = time.time() - start_time

    print(f"Tyler's imp: {custom_imp_run_time} ms\nWhisperx imp: {whisperx_run_time}")
    # Tyler's imp: 49535.377979278564 ms
    # Whisperx imp: 16695.17493247986
