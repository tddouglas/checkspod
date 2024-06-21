from analyze_text import local_analysis
from audio_to_text import audio_to_text, whisperx_diarization_transcribe
from dotenv import load_dotenv
from checkspod_api.checkspod_downloader import checkspod_pipeline
from database.database_connector import iterate_episodes
from database.model import Episodes
import time

from helpers.text_file_helper import write_to_text_file


# Runtime comparison for whisperx vs custom implementation
def custom_vs_whisperx_runtime(episode: Episodes):
    start_time = time.time()
    transcript_tyler = audio_to_text(episode.filename, True)
    tyler_imp_run_time = time.time() - start_time
    start_time = time.time()
    transcript_whisper = whisperx_diarization_transcribe(episode.filename)
    whisperx_run_time = time.time() - start_time

    print(f"Tyler's imp: {tyler_imp_run_time} ms\nWhisperx imp: {whisperx_run_time}")
    # Tyler's imp: 49535.377979278564 ms
    # Whisperx imp: 16695.17493247986


if __name__ == '__main__':
    # checkspod_download = checkspod_pipeline()
    # if checkspod_download:
    #     pass

    load_dotenv()

    for episode in iterate_episodes(10):
        print(f'Title: {episode.title}, Description:\n {episode.summary}')


        # transcript = audio_to_text(episodes.filename, True)
        # transcript = whisperx_diarization_transcribe(episodes.filename)
        # print(transcript)
        # full_filename = 'checkspod_files/reviewed_transcripts/' + episodes.filename + '.txt'
        # write_to_text_file(transcript, full_filename)


        # after diarlization, should update db to store that fact
        # update_query = Episodes.update(summary=new_summary).where(Episodes.id == episodes.id)
        # update_query.execute()
