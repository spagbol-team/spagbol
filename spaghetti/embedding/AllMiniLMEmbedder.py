"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import numpy as np

from spaghetti.embedding.Embedder import Embedder

class AllMiniLMEmbedder(Embedder):
    """
    Embedder for all-MiniLM-L6-v2 model. This class is responsible for loading the model and tokenizer,
    and performing mean pooling on the model's output to generate sentence embeddings.
    """

    def __init__(self):
        try:
            self._model = self._init_model()
            self._tokenizer = self._init_tokenizer()
        except Exception as e:
            print(f"Error initializing model or tokenizer: {e}")

    def _init_model(self):
        """
        This method initializes the model
        """
        try:
            return AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Error initializing model: {e}")
            return None

    def _init_tokenizer(self):
        """
        This method initializes the tokenizer
        """
        try:
            return AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Error initializing tokenizer: {e}")
            return None

    def embed(self, data: str) -> np.array:
        """
        This method should embed the input data
        :param data: Input data to be embedded
        :return: Embedded data
        """
        try:
            # Tokenize the input data
            inputs = self._tokenizer(data, return_tensors='pt', truncation=True, padding=True)

            # Get the model's output
            model_output = self._model(**inputs)

            # Perform mean pooling on the model's output to generate sentence embeddings
            embeddings = self._mean_pooling(model_output, inputs['attention_mask'])

            return embeddings.detach().numpy()
        except Exception as e:
            print(f"Error embedding data: {e}")
            return None

    def embed_batch(self, data: list[str]) -> np.array:
        """
        This method should embed the input data in batches
        :param data: Input data to be embedded
        :return: Embedded data
        """
        try:
            # Tokenize the input data
            inputs = self._tokenizer(data, return_tensors='pt', truncation=True, padding=True)

            # Get the model's output
            model_output = self._model(**inputs)

            # Perform mean pooling on the model's output to generate sentence embeddings
            embeddings = self._mean_pooling(model_output, inputs['attention_mask'])

            return embeddings.detach().numpy()
        except Exception as e:
            print(f"Error embedding batch data: {e}")
            return None

    def _mean_pooling(self, model_output: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """
        Performs mean pooling on the model's output to generate sentence embeddings.
        Takes into account attention mask for correct averaging.

        :param model_output: The output from the all-MiniLM-L6-v2 model.
        :param attention_mask: The attention mask generated during tokenization.
        :return: The sentence embeddings.
        """
        try:
            token_embeddings = model_output[0]
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        except Exception as e:
            print(f"Error during mean pooling: {e}")
            return None
