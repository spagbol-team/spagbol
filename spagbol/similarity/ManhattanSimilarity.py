"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
from typing import Iterable, List

from spagbol.similarity import SimilarityMeasure


class ManhattanSimilarity(SimilarityMeasure):
    """
    Object for computation of Manhattan Similarity. NOTE values sign is inverted to convert dissimilarity
    that is computed with Manhattan distance into a similarity.
    Example usages:
        embedding_1 = EmbeddingFunction(data)
        embedding_2 = EmbeddingFunction(some_data)
        similarity = ManhattanSimilarity.compute(embedding_1, embedding_2)
    """

    @staticmethod
    def compute(embedding_1: Iterable, embedding_2: Iterable) -> float:
        """
        Computes Manhattan similarity between embedding_1 and embedding_2

        :param embedding_1: First of the embedding pair for similarity computation
        :param embedding_2: Second of the embedding pair for similarity computation
        :raises ValueError: When embedding shapes are not equal
        :return: Manhattan similarity value between embedding_1 and embedding_2
        """
        embedding_1 = np.array(embedding_1)
        embedding_2 = np.array(embedding_2)
        if embedding_1.shape != embedding_2.shape:
            raise ValueError("Embedding shapes are incompatible")
        similarity: float = - np.sum(abs(embedding_1 - embedding_2))
        return similarity

    @staticmethod
    def compute_batch(comparate_embedding: Iterable, comparand_embeddings: Iterable) -> List[float]:
        """
        Computes manhattan similarity between a one-dimensional embedding and a vertically stacked batch of
        one-dimensional embeddings. Shapes must be [n] and [m, n].

        :param comparate_embedding: Singular embedding that will be compared to a batch
        :param comparand_embeddings: Batch of embeddings that will be used to compute similarity with a comparate
        :return: List of manhattan similarities between comparate_embedding and all embeddings in comparand_embeddings
        """
        comparate_embedding = np.array(comparate_embedding)
        comparand_embeddings = np.array(comparand_embeddings)
        if len(comparate_embedding.shape) != 1:
            raise ValueError("Embedding has to be one-dimensional, squeeze or flatten other dimensions")
        if len(comparand_embeddings.shape) != 2:
            raise ValueError("comparand_embeddings must be a stack of one-dimensional embeddings")
        if comparate_embedding.shape[0] != comparand_embeddings.shape[1]:
            raise ValueError("Comparate embeddings and stacked embeddings in"
                             " comparand_embeddings must have the same shape")

        similarities = - np.sum(abs(comparand_embeddings - comparate_embedding), axis=1)
        return similarities.tolist()
