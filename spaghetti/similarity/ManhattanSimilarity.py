"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

import numpy as np
from typing import Iterable, List

from spaghetti.similarity import SimilarityMeasure


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
