"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import List


class SimilarityMeasure(ABC):
    """
    This is an interface for all similarity measures used with Spaghetti standalone app.
    """

    @staticmethod
    @abstractmethod
    def compute(embedding_1: Iterable, embedding_2: Iterable) -> float:
        """
        Has to compute similarity between two iterable embeddings.
        Used in search and visualization modules

        :param embedding_1: First of the embedding pair for similarity computation
        :param embedding_2: Second of the embedding pair for similarity computation
        :return:
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def compute_batch(comparate_embedding: Iterable, comparand_embeddings: Iterable) -> List[float]:
        """
        Has to compute similarity between singular comparate_embedding and a batch of comparand embeddings

        :param comparate_embedding: Singular embedding that will be compared to a batch
        :param comparand_embeddings: Batch of embeddings that will be used to compute similarity with a comparate
        :return: List of similarity values between comparate_embedding and all embeddings in comparand_embeddings
        """
        raise NotImplementedError
