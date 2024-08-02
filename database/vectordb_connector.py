import logging
from typing import Tuple
import faiss
import numpy as np

from database.model import Embeddings
from database.sqldb_connector import fetch_embeddings_for_episode

EMBEDDING_FILE = 'embeddings.index'
logger = logging.getLogger(__name__)


def write_embedding(embedding: np.ndarray, episode_id: int) -> None:
    """
    Write embedding to disk file.
    TODO: Write embedding id from embeddings.index file to proper location in SQLite
    Look into faiss-gpu if search is too slow.
    @param embedding: Python ndarray representing a speaker
    @param episode_id: Episode ID
    """
    embedding = normalize(embedding)
    try:
        index = faiss.read_index(EMBEDDING_FILE)
    except RuntimeError as e:
        logger.debug(f"Faiss FileIOReader Runtime Error:\n${e}")
        logger.warning("No existing vector DB found. Creating new embedding database.")
        vector_dim = embedding.shape[1]

        # Build the index for inner product search. Inner product search on normalized vectors = cosine similarity search
        index = faiss.IndexFlatIP(vector_dim)

    existing_stored_embeddings = fetch_embeddings_for_episode(episode_id)
    # If we've already stored embeddings for this episode, find the most similar stored embedding to the embedding we are
    # writing. Then delete that embedding from the vector db
    if existing_stored_embeddings:
        logger.info("Embeddings have been stored for this episode already")
        embedding_index = 1
        vector_to_replace = None
        for stored_embedding_index, stored_embedding_participant_id in existing_stored_embeddings:
            stored_embedding = index.reconstruct(stored_embedding_index).reshape(1, -1)
            x = embedding_similarity(stored_embedding, embedding)
            if x < embedding_index:
                embedding_index = x
                vector_to_replace = stored_embedding_index
        # TODO: Delete `vector_to_replace` in DB

    current_size = index.ntotal
    index.add(embedding)
    faiss.write_index(index, EMBEDDING_FILE)
    # TODO: Only write embedding if one doesn't exist already.
    Embeddings.create(embedding_index=current_size, participant="Unknown", episode="Unknown")


def search_embeddings(query_embedding: np.ndarray, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Search existing embedding DB for the most similar embedding
    @param k: The number of nearest neighbors to retrieve.
    @param query_embedding: Python ndarray representing a speaker
    @return: Indices and distances of the most similar embeddings.
    """
    query_embedding = normalize(query_embedding)
    index = faiss.read_index(EMBEDDING_FILE)
    d, i = index.search(query_embedding, k)  # D is the inner product scores, I is the indices of the closest vectors
    return i, d


def find_similar_embeddings_by_index(embedding_index: int, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Find the most similar embedding to a given embedding index in the FAISS vector store.
    @param embedding_index: index of embedding in FAISS vector store.
    @param k: The number of nearest neighbors to retrieve.
    @return: Indices and distances of the most similar embeddings.
    """
    index = faiss.read_index(EMBEDDING_FILE)
    query_vector = index.reconstruct(embedding_index).reshape(1, -1)  # Retrieve the vector from the index
    return search_embeddings(query_vector, k)


def embedding_similarity(x: np.ndarray, y: np.ndarray) -> float:
    """
    Compute the similarity between two vectors. Returns float between 0 and 1 representing the cosine similarity.
    0 being the most similar and 1 being the most dissimilar.
    @param x: Embedding vector as (np.ndarray)
    @param y: Embedding vector as (np.ndarray)
    @return: Cosine similarity between two vectors.
    """
    dot_product = np.dot(x, y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    return dot_product / (norm_x * norm_y)


def normalize(embedding: np.ndarray) -> np.ndarray:
    """
    Normalize input vector to unit length. If already normalized, just return the vector.
    @param embedding: Python ndarray representing a speaker
    @return: Normalized vector representing a speaker
    """
    embedding = embedding.reshape(1, -1)
    norms = np.linalg.norm(embedding, axis=1)
    if not np.allclose(norms, 1):
        embedding = embedding / norms[:, np.newaxis]
    return embedding
