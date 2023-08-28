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

from spaghetti.embedding.Embedder import Embedder

class AllMiniLMEmbedder:
    """
    Embedder for all-MiniLM-L6-v2 model. This class is responsible for loading the model and tokenizer,
    and performing mean pooling on the model's output to generate sentence embeddings.
    Example usages:
        embedder = AllMiniLMEmbedder()
        sentence_embeddings = embedder._mean_pooling(model_output, attention_mask)

    :param _model: The all-MiniLM-L6-v2 model loaded from HuggingFace Hub.
    :param _tokenizer: The tokenizer corresponding to the all-MiniLM-L6-v2 model.
    """

    def __init__(self):
        """
        Initializes the model and tokenizer.
        """
        self._model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self._tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    def _mean_pooling(self, model_output: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """
        Performs mean pooling on the model's output to generate sentence embeddings.
        Takes into account attention mask for correct averaging.

        :param model_output: The output from the all-MiniLM-L6-v2 model.
        :param attention_mask: The attention mask generated during tokenization.
        :return: The sentence embeddings.
        """
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

