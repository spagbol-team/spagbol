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
import numpy as np

class Embedder(ABC):
    """
    This is the interface for all embedding techniques used in this project.
    Every embedding class imported into this project has to use this interface
    """

    @abstractmethod
    def __init__(self):
        self._model = self._init_model()
        self._tokenizer = self._init_tokenizer()

    @abstractmethod
    def _init_model(self):
        """
        This method should initialize the model
        """
        raise NotImplementedError()

    @abstractmethod
    def _init_tokenizer(self):
        """
        This method should initialize the tokenizer
        """
        raise NotImplementedError()

    @abstractmethod
    def embed(self, data: str) -> np.array:
        """
        This method should embed the input data
        :param data: Input data to be embedded
        :return: Embedded data
        """
        raise NotImplementedError()

    @abstractmethod
    def embed_batch(self, data: list[str]) -> np.array:
        """
        This method should embed the input data in batches
        :param data: Input data to be embedded
        :return: Embedded data
        """
        raise NotImplementedError()

    