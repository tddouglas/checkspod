from analyze_text import local_analysis
from audio_to_text import audio_to_text, whisperx_diarization_transcribe
from dotenv import load_dotenv
from checkspod_api.checkspod_downloader import checkspod_pipeline
from database.model import Episodes
import time

def read_in_txt(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()
    return content

if __name__ == '__main__':
    # checkspod_download = checkspod_pipeline()
    # if checkspod_download:
    #     pass

    load_dotenv()
    # TODO: Iterate over entire database and produce rttm files.
    # This means I have to scrape summary for # of speakers to get proper outputs.
    query = Episodes.select()
    for x, episodes in enumerate(query):
        if x > 0:
            break

        # audio_to_text(episodes.filename, True)
        # transcript = whisperx_diarization_transcribe(episodes.filename)
        prompt = read_in_txt('test_prompt.txt')
        local_analysis(prompt)

        # print(f"Tyler's imp: {tyler_imp_run_time} ms\nWhisperx imp: {whisperx_run_time}")
        # Tyler's imp: 49535.377979278564 ms
        # Whisperx imp: 16695.17493247986

        # after diarlization, should update db to store that fact
        # update_query = Episodes.update(summary=new_summary).where(Episodes.id == episodes.id)
        # update_query.execute()
