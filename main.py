from pydub import AudioSegment
from checkspod_downloader import query_checkspod
from audio_file_manipulator import mp3_to_wav_pipeline
from audio_to_text import audio_to_text, audio_diarization


if __name__ == '__main__':
    # query_checkspod()
    # mp3_to_wav_pipeline("0ba4eb49-b9a5-41b7-8610-65e80fcf9276")
    audio_to_text("0ba4eb49-b9a5-41b7-8610-65e80fcf9276", True)
