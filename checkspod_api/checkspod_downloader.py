from checkspod_api.checkspod_api_models import APIEpisodeResponse, APIEpisode
from database.model import Episodes
from typing import List
from pydantic import ValidationError
import os
import requests as r
from bs4 import BeautifulSoup
from helpers.audio_file_helper import mp3_to_wav_pipeline

# This is a script to iterate through all Checks & Balance episodes, pull the details page for the list overview,
# then query the details page to pull the associated .mp3 file from the only media request on the details page
# Should pull all files from January 17th, 2020 onward = 183 episodes. Episodes dynamic load so will need to solve
# How to get all episodes loaded on page to parse


CHECKSPOD_EPISODES_JSON = "https://shows.acast.com/api/shows/57cc3c7d-b0fd-4930-9279-4e84c75df457/episodes?paginate=false&results=400"


def query_checkspod() -> APIEpisodeResponse:
    try:
        episode_list = r.get(CHECKSPOD_EPISODES_JSON).json()["results"]
        validated_list = APIEpisodeResponse(responses=episode_list)
        return validated_list
    except r.exceptions.RequestException as e:
        print(f"Error while querying checkspod API:\n{e}")
    except ValidationError as e:
        print(f"Error while validating checkspod API schema:\n{e}")


def new_episodes_available() -> List[APIEpisode]:
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


def download_episode(episode_list: List[APIEpisode], max_downloads: int = 0):
    for x, episode in enumerate(episode_list):
        # Check if we've already downloaded the max number of files we want. This is for testing purposes.
        if max_downloads != 0 and x > 0:
            break

        filename_base = episode.publish_date[:10]
        filename_extension = filename_base + '.mp3'
        full_filename = 'checkspod_files/original_audio/' + filename_extension

        if not os.path.isfile(full_filename):  # If file doesn't already exist
            url = episode["audio"]["url"]
            queryable_url = 'https://' + url.replace("//s3.amazonaws.com/", "")
            doc = r.get(queryable_url)
            if doc.status_code == 200:
                if store_file(full_filename, doc.content):
                    try:
                        soup = BeautifulSoup(episode["summary"], "html.parser")
                        stripped_summary = soup.get_text()  # Convert HTML summary to text
                        new_episode = Episodes.create(title=episode["title"], publish_date=episode["publishDate"],
                                                      summary=stripped_summary, filename=filename_base,
                                                      size=episode["audio"]["size"], url=queryable_url,
                                                      duration=episode["duration"])
                        print("episode created successfully in DB")

                        new_filename_base = filename_base + '-' + str(new_episode.id)
                        new_filename = 'checkspod_files/original_audio/' + new_filename_base + 'mp3'
                        os.rename(full_filename, new_filename)  # Rename file to include db id

                        # Format original audio -> WAV
                        wav_filename = new_filename_base + '.wav'
                        dest_wav_filename = 'checkspod_files/' + wav_filename
                        mp3_to_wav_pipeline(full_filename, dest_wav_filename)
                        update_query = Episodes.update(filename=new_filename_base).where(Episodes.id == new_episode.id)
                        update_query.execute()
                    except KeyError as e:
                        print(f"Error creating episode. Missing required field/\n{e}")
                        remove_file(full_filename)
            else:
                print("Checkspod audio download failed")
        else:
            print("File already present. Something must have gone wrong fetching latest episodes.")


def store_file(filename, content) -> bool:
    success = False
    try:
        with open(filename, 'wb') as f:
            f.write(content)
        success = True
    except IOError as e:
        # Handles exceptions raised by file operations (e.g., file not found, disk full, etc.)
        print(f"An error occurred while writing the file: {e}")
    except Exception as e:
        # This is a more general exception to catch any other exceptions that may occur
        print(f"An unexpected error occurred: {e}")
    finally:
        return success


def remove_file(filename):
    if filename.startswith("checkspod_files/") and len(filename) > 16:
        os.remove(filename)


'''
Returns true if there are episodes to download and they were downloaded successfully.
'''


def checkspod_pipeline() -> bool:
    success = False
    try:
        available_episodes = new_episodes_available()
        if available_episodes:
            download_episode(available_episodes)
            success = True
    except Exception as e:
        print(f"An error occurred while downloading latest checkspod eps:\n{e}")
    finally:
        return success
