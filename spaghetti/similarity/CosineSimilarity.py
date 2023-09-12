"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

from typing import Iterable, List
import numpy as np
from numpy.linalg import norm

from spaghetti.similarity import SimilarityMeasure


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

