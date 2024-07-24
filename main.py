import argparse
import logging
from dotenv import load_dotenv

from audio.audio_pipeline import audio_pipeline
from audio.diarization.benchmark import pyannote_vs_whisperx_runtime
from audio.diarization.pipeline import diarization_pipeline
from audio.verification.compare_speakers import compare_all_embeddings
from checkspod_api.checkspod_downloader import checkspod_pipeline
from database.sqldb_connector import iterate_episodes
from helpers.logger import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download and Transcriber of the Checks & Balances podcast by The Economist')
    parser.add_argument('action', type=str, help='Action to perform',
                        choices=['pipeline-update', 'runtime-comparison', 'pyannote-transcribe',
                                 'whisperx-transcribe', 'test'], )
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
                pyannote_vs_whisperx_runtime(episode)
        case "pyannote-transcribe":
            logger.debug("Custom transcribe file started")
            for episode in iterate_episodes(args.number_of_episodes):
                logger.info(f'Title: {episode.title}, Description:\n {episode.summary}')
                transcript = audio_pipeline(episode.filename, "pyannote", False, "whisperx", False, None)
                print(transcript)
        case "whisperx-transcribe":
            logger.debug("Whisperx transcribe file started")
            for episode in iterate_episodes(args.number_of_episodes):
                logger.info(f'Title: {episode.title}, Description:\n {episode.summary}')
                transcript = audio_pipeline(episode.filename, "whisperx", False, "whisperx", False, None)
                print(transcript)
        case "test":
            embeddings = {}
            for episode in iterate_episodes(args.number_of_episodes):
                annotation, embedding = diarization_pipeline(episode.filename, "pyannote", False)
                embeddings[episode.filename] = embedding
            print(compare_all_embeddings(embeddings))
        case "_":
            logger.warning("No valid argument provided")
