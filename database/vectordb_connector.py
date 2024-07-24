import logging
from typing import Tuple

import faiss
import numpy as np

EMBEDDING_FILE = 'embeddings.index'
logger = logging.getLogger(__name__)


def write_embedding(embedding: np.ndarray):
    """
    Write embedding to disk file.
    TODO: Write embedding id from embeddings.index file to proper location in SQLite
    Look into faiss-gpu if search is too slow.
    @param embedding: Python ndarray representing a speaker
    """
    embedding = normalize(embedding)

    try:
        index = faiss.read_index(EMBEDDING_FILE)
    except Exception as e:
        print("Exception triggered. Specify l:22 of vectordb_connector file", e)
        logger.warning("Creating new embedding database")
        vector_dim = embedding.shape[1]
        index = faiss.IndexFlatIP(vector_dim)

    index.add(embedding)
    faiss.write_index(index, EMBEDDING_FILE)


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


def normalize(embedding: np.ndarray) -> np.ndarray:
    """
    Normalize input vector to unit length. If already normalized, just return the vector.
    @param embedding: Python ndarray representing a speaker
    @return: Normalized vector representing a speaker
    """
    norms = np.linalg.norm(embedding, axis=1)
    if not np.allclose(norms, 1):
        embedding = embedding / norms[:, np.newaxis]
    return embedding
