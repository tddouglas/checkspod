import logging

import numpy as np
from scipy.spatial.distance import cdist

logger = logging.getLogger(__name__)


def compare_two_embeddings(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Calculates cosine distance between pairs of vectors.
    Low distance (close to 0) means the angle of embeddings is small. This means they are pointing in the same direction
    indicating high similarity between speakers.
    High Distance (close to 1) means the embeddings are orthogonal, indicating low similarity.
    @param embedding1: ndarray representing a speaker
    @param embedding2: ndarray representing a speaker
    @return: float representing cosine distance between embedding1 and embedding2
    """
    return cdist(embedding1.reshape(1, -1), embedding2.reshape(1, -1), metric="cosine")[0, 0]


def compare_all_embeddings(embeddings):
    keys = list(embeddings.keys())
    n = len(keys)
    comparisons = {1: [], 2: [], 3: []}

    for i in range(n):
        for j in range(i + 1, n):
            key1, key2 = keys[i], keys[j]
            array1, array2 = embeddings[key1], embeddings[key2]
            for idx in range(3):
                comparisons[idx + 1].append((compare_two_embeddings(array1[idx], array2[idx]), key1, key2))

    return comparisons
