import argparse
import logging
from dotenv import load_dotenv

from audio_to_text.diarization.benchmark import custom_vs_whisperx_runtime
from audio_to_text.diarization.custom import audio_to_text
from audio_to_text.diarization.whisperx import whisperx_diarization_transcribe
from checkspod_api.checkspod_downloader import checkspod_pipeline
from database.database_connector import iterate_episodes
from helpers.logger import setup_logging
from helpers.txt_file_helper import write_to_text_file


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download and Transcriber of the Checks & Balances podcast by The Economist')
    parser.add_argument('action', type=str, help='Action to perform',
                        choices=['pipeline-update', 'runtime-comparison', 'custom-transcribe-file',
                                 'whisperx-transcribe-file'], )
    parser.add_argument('number_of_episodes', type=int,
                        help='Number of episodes to perform action on (when applicable)')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    load_dotenv()
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Main script started")

    match args.action:
        case "pipeline-update":
            logger.debug("Pipeline update started")
            checkspod_download_res = checkspod_pipeline()
            if checkspod_download_res:
                print("Successfully downloaded latest episodes")
        case "runtime-comparison":
            logger.debug("Runtime comparison started")
            for episode in iterate_episodes(args.number_of_episodes):
                custom_vs_whisperx_runtime(episode)
        case "custom-transcribe-file":
            logger.debug("Custom transcribe file started")
            for episode in iterate_episodes(args.number_of_episodes):
                logger.info(f'Title: {episode.title}, Description:\n {episode.summary}')
                transcript = audio_to_text(episode.filename, True)
                print(transcript)
        case "whisperx-transcribe-file":
            logger.debug("Whisperx transcribe file started")
            for episode in iterate_episodes(args.number_of_episodes):
                logger.info(f'Title: {episode.title}, Description:\n {episode.summary}')
                transcript = whisperx_diarization_transcribe(episode.filename)
                print(transcript)

                full_filename = 'checkspod_files/reviewed_transcripts/' + episode.filename + '.txt'
                write_to_text_file(transcript, full_filename)
        case "_":
            logger.debug("No valid argument provided")
