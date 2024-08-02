import logging
import os
import sys
import requests as r
from bs4 import BeautifulSoup
from typing import List
from pydantic import ValidationError

from checkspod_api.checkspod_api_models import APIEpisodeResponse, APIEpisode
from database.model import Episodes
from helpers.audio_file_helper import mp3_to_wav_pipeline, construct_mp3_path, construct_wav_path
from helpers.file_helper import get_base_path

logger = logging.getLogger(__name__)

# This is a script to iterate through all Checks & Balance episodes, pull the details page for the list overview,
# then query the details page to pull the associated .mp3 file from the only media request on the details page
# Should pull all files from January 17th, 2020 onward = 183 episodes. Episodes dynamic load so will need to solve
# How to get all episodes loaded on page to parse


CHECKSPOD_EPISODES_JSON = "https://shows.acast.com/api/shows/57cc3c7d-b0fd-4930-9279-4e84c75df457/episodes?paginate=false&results=400"


def query_checkspod() -> APIEpisodeResponse:
    """
    Query checkspod API and validate response against expected schema.
    @return: List of APIEpisodes
    """
    try:
        # TODO: Economist went private and acast changed their format :(
        # Check postman, new implementation will need to filter through sphinx.acast link with active cookie and download each episode by replacing ep_id with next ep_id
        episode_list = r.get(CHECKSPOD_EPISODES_JSON).json()["results"]
        validated_list = APIEpisodeResponse(responses=episode_list)
        return validated_list
    except r.exceptions.RequestException as e:
        logger.critical(f"Error while querying checkspod API:\n{e}")
        sys.exit(1)
    except ValidationError as e:
        logger.critical(f"Error while validating checkspod API schema:\n{e}")
        sys.exit(1)


def new_episodes_available() -> List[APIEpisode]:
    """
    Compare query result episode list to episode table. Add any episodes with a more recent publish date than the most
    recent episodes in the episode table.
    @return: List of episodes added to episodes table. Empty if no episodes were added.
    """
    res = []
    checkspod_list = query_checkspod()
    most_recent_episode = checkspod_list.results[0]
    latest_db_episode = Episodes.select().order_by(Episodes.publish_date.desc()).get()
    if most_recent_episode.publish_date != latest_db_episode.publish_date:  # There are episodes to download
        for episode in checkspod_list.results:
            if episode.publish_date <= latest_db_episode.publish_date:
                break
            res.append(episode)
    return res


def download_episodes(episode_list: List[APIEpisode], max_downloads: int):
    for x, episode in enumerate(episode_list):
        # Check if we've already downloaded the max number of files we want. This is for testing purposes.
        if max_downloads != 0 and x > 0:
            break

        filename_base = episode.publish_date[:10]
        full_filename = construct_mp3_path(filename_base)
        if not os.path.isfile(full_filename):  # If file doesn't already exist
            url = episode["audio"]["url"]
            queryable_url = 'https://' + url.replace("//s3.amazonaws.com/", "")
            doc = r.get(queryable_url)
            if doc.status_code == 200:
                if store_file(full_filename, doc.content):
                    try:
                        # Scrape relevant fields and write data to db
                        soup = BeautifulSoup(episode["summary"], "html.parser")
                        stripped_summary = soup.get_text()  # Convert HTML summary to text
                        new_episode = Episodes.create(title=episode["title"], publish_date=episode["publishDate"],
                                                      summary=stripped_summary, filename=filename_base,
                                                      size=episode["audio"]["size"], url=queryable_url,
                                                      duration=episode["duration"])
                        logger.info(f"Episode - ${episode['title']} - created successfully in DB")

                        filename_base_db_id = filename_base + '-' + str(new_episode.id)
                        full_filename_db_id = construct_mp3_path(filename_base_db_id)
                        os.rename(full_filename, full_filename_db_id)  # Rename file to include db id

                        # Format original audio -> WAV
                        wav_filename = construct_wav_path(filename_base_db_id)
                        mp3_to_wav_pipeline(full_filename, wav_filename)
                        update_query = Episodes.update(filename=filename_base_db_id).where(
                            Episodes.id == new_episode.id)
                        update_query.execute()
                    except KeyError as e:
                        logger.critical(f"Error creating episode. Missing required field/\n{e}")
                        remove_file(full_filename)
            else:
                logger.critical("Checkspod audio download failed")
        else:
            logger.error("File already present. Something must have gone wrong fetching latest episodes.")


def store_file(filename, content) -> bool:
    success = False
    try:
        with open(filename, 'wb') as f:
            f.write(content)
        success = True
    except IOError as e:
        # Handles exceptions raised by file operations (e.g., file not found, disk full, etc.)
        logger.critical(f"An error occurred while writing the file: {e}")
    except Exception as e:
        # This is a more general exception to catch any other exceptions that may occur
        logger.critical(f"An unexpected error occurred: {e}")
    finally:
        return success


def remove_file(filename):
    audio_base_path = get_base_path()
    if filename.startswith(audio_base_path) and len(filename) > len(audio_base_path):
        os.remove(filename)


def checkspod_pipeline(max_downloads: int = 0) -> bool:
    """
    Query checkspod API. If there are new episodes available, download them.
    @return: True if new episodes were downloaded. False otherwise.
    """
    success = False
    try:
        available_episodes = new_episodes_available()
        if available_episodes:
            download_episodes(available_episodes, max_downloads)
            success = True
    except Exception as e:
        print(f"An error occurred while downloading latest checkspod eps:\n{e}")
    finally:
        return success
