"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Iterable, List
import numpy as np
from numpy.linalg import norm

from spagbol.similarity import SimilarityMeasure


class CosineSimilarity(SimilarityMeasure):
    """
    Object for computation of Cosine Similarity.
    Example usages:
        For single values:
            embedding_1 = EmbeddingFunction(data)
            embedding_2 = EmbeddingFunction(some_data)
            similarity = CosineSimilarity.compute(embedding_1, embedding_2)
        For batch:
            embedding = EmbeddingFunction(data) # Shape (n,)
            stacked_embeddings = EmbeddingFunction(stacked_data) # Shape (m, n)
            similarities = compute_batch(embedding, stacked_embeddings) # Out shape - (m,)
    """

    @staticmethod
    def compute(embedding_1: Iterable, embedding_2: Iterable) -> float:
        """
        Computes similarity between two arrays of embeddings. Embeddings must have aligning shapes,
        e.g. for two-dimensional array embedding_1 with shape [384, 1] aligning embedding_2 shape is [1, 384]

        :param embedding_1: First of the embedding pair for similarity computation
        :param embedding_2: Second of the embedding pair for similarity computation
        :raises ZeroDivisionError: if np.linalg.norm(embedding_1) == 0 or np.linalg.norm(embedding_2) == 0
        :raises ValueError: if shapes of embeddings don't align, e.g. shape of embedding_1 is [384, 1] and
                            shape of embedding_2 is [384, 2]
        :raises TypeError: if embedding_1 or embedding_2 are not instances of Iterable
        :return: Cosine similarity between embedding_1 and embedding_2. Similarity values are in range [-1, 1]
        """
        if not isinstance(embedding_1, Iterable) or not isinstance(embedding_2, Iterable):
            raise TypeError("Embeddings must be iterable")

        return np.dot(embedding_1, embedding_2) / (norm(embedding_1) * norm(embedding_2))

    @staticmethod
    def compute_batch(comparate_embedding: Iterable, comparand_embeddings: Iterable) -> List[float]:
        """
        Computes cosine similarity between a one-dimensional embedding and a vertically stacked batch of
        one-dimensional embeddings. Shapes must be [n] and [m, n].

        :param comparate_embedding: Singular embedding that will be compared to a batch
        :param comparand_embeddings: Batch of embeddings that will be used to compute similarity with a comparate
        :raises ZeroDivisionError: if np.linalg.norm(comparate_embedding) == 0 or
                np.linalg.norm(comparand_embeddings, axis=1) == 0
        :raises ValueError: is dim 0 shape of comparand_embeddings != dim 0 shape of comparate_embedding
        :return: List of cosine similarities between comparate_embedding and all embeddings in comparand_embeddings
        """

        if not isinstance(comparate_embedding, Iterable) or not isinstance(comparand_embeddings, Iterable):
            raise TypeError("Embeddings must be iterable")

        return (np.dot(comparand_embeddings, comparate_embedding) / (norm(comparate_embedding) *
                                                                     norm(comparand_embeddings, axis=1))).tolist()

