"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import numpy as np

from tqdm import tqdm

from typing import List

from spagbol.embedding.Embedder import Embedder

import logging

class AllMiniLMEmbedder(Embedder):
    """
    Embedder for all-MiniLM-L6-v2 model. This class is responsible for loading the model and tokenizer,
    and performing mean pooling on the model's output to generate sentence embeddings.
    """

    def __init__(self):
        try:
            self._device = "cpu"
            if torch.cuda.is_available():
                self._device = "cuda"
            self._model = self._init_model().to(self._device)
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
            inputs = self._tokenizer(data, return_tensors='pt', truncation=True, padding=True).to(self._device)

            # Get the model's output
            model_output = self._model(**inputs)

            # Perform mean pooling on the model's output to generate sentence embeddings
            embeddings = self._mean_pooling(model_output, inputs['attention_mask'])

            embeddings = F.normalize(embeddings, p=2, dim=1)

            return embeddings.detach().numpy()
        except Exception as e:
            print(f"Error embedding data: {e}")
            return None

    def embed_batch(self, data: List[str]) -> np.array:
        """
        Embeds the input data in batches with a progress bar.
        
        This method processes each sentence in the input data individually, 
        applies the embedding model, and returns the embeddings as a numpy array.
        A progress bar from tqdm is displayed to monitor the embedding process.
        
        :param data: List of input sentences to be embedded.
        :return: A numpy array of sentence embeddings.
        """
        embeddings_list = []
        # Process each sentence individually and update the progress bar
        for sentence in tqdm(data, desc="Embedding sentences"):
            try:
                # Tokenize the input sentence
                inputs = self._tokenizer([sentence], return_tensors='pt', truncation=True, padding=True).to(self._device)
                # Get the model's output
                model_output = self._model(**inputs).last_hidden_state.cpu()
                # Perform mean pooling on the model's output to generate sentence embeddings
                embeddings = self._mean_pooling(model_output, inputs['attention_mask'])
                # Normalize the embeddings
                normalized_embeddings = F.normalize(embeddings, p=2, dim=1)
                # Append the embeddings to the list
                embeddings_list.append(normalized_embeddings.detach().numpy())
            except Exception as e:
                logging.debug(f"Error embedding sentence: {e}")
                print(f"Error embedding sentence: {e}")
                # Optionally, append None or handle the error differently
        # Concatenate all sentence embeddings into a single numpy array
        return np.concatenate(embeddings_list, axis=0)

    def _mean_pooling(self, model_output: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """
        Performs mean pooling on the model's output to generate sentence embeddings.
        Takes into account attention mask for correct averaging.

        :param model_output: The output from the all-MiniLM-L6-v2 model.
        :param attention_mask: The attention mask generated during tokenization.
        :return: The sentence embeddings.
        """
        try:
            token_embeddings = model_output  # Assuming model_output is already the last_hidden_state tensor
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
            sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            return sum_embeddings / sum_mask
        except Exception as e:
            print(f"Error during mean pooling: {e}")
            return None
