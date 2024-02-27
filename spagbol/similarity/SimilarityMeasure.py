"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
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
