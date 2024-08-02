import logging
import sqlite3
from typing import Generator, List, Tuple

from bs4 import BeautifulSoup
from database.model import Episodes, Embeddings

logger = logging.getLogger(__name__)

try:
    # Connect to the database file (it will create the file if it doesn't exist)
    conn = sqlite3.connect('database/checkspod.db')

    # Create a cursor object
    cur = conn.cursor()

except sqlite3.Error as e:
    print(f"Error while connecting to DB:\n{e}")


def iterate_episodes(limit=0) -> Generator[Episodes, None, None]:
    query = Episodes.select()
    for x, episode in enumerate(query):
        if limit and x == limit:
            break
        yield episode


def fetch_embeddings_for_episode(episode_id: int) -> List[Tuple[Embeddings.embedding_index, Embeddings.participant]]:
    query = (Embeddings
             .select(Embeddings.embedding_index, Embeddings.participant)
             .where(Embeddings.episode == episode_id))

    # Iterate through the results
    for embedding in query:
        logger.info(
            f'Embedding Index: {embedding.embedding_index}, Participant ID: {embedding.participant.id if embedding.participant else "Unknown"}')

    return [(embedding.embedding_index, embedding.participant.id) for embedding in query]

def close_connection():
    conn.close()

# Boilerplate for row insert
# def insert_row(column_name_tuple, tuple_to_insert):
#     # Insert a row of data
#     cur.execute("INSERT INTO episodes (name, value) VALUES ('SampleName', 'SampleValue')")
#
#     # Save (commit) the changes
#     conn.commit()


# Boilerplate to iterate through every row of table and perform some update
# def update_every_entry():
#     query = Episodes.select()
#     for episodes in query:
#         soup = BeautifulSoup(episodes.summary)
#         new_summary = soup.get_text()
#
#         update_query = Episodes.update(summary=new_summary).where(Episodes.id == episodes.id)
#         update_query.execute()
