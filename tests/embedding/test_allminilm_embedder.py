"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""
import unittest
import torch
from spaghetti.embedding.AllMiniLMEmbedder import AllMiniLMEmbedder

embedder = AllMiniLMEmbedder()


# you can run this test using the following command line call
# python -m unittest tests.embedding.test_allminilm_embedder

def test_mean_pooling():
    # Create a dummy model output and attention mask
    model_output = (torch.randn(2, 3, 4),)
    attention_mask = torch.tensor([[1, 1, 0], [1, 0, 0]])

    # Expected result is the mean of the embeddings of the actual tokens
    expected_result = torch.sum(model_output[0] * attention_mask.unsqueeze(-1), dim=1) / torch.clamp(attention_mask.sum(dim=1, keepdim=True), min=1e-9)

    # Check if the method returns the expected result
    result = embedder._mean_pooling(model_output, attention_mask)
    assert torch.allclose(result, expected_result)

    # Check if the method handles edge cases correctly
    attention_mask_zero = torch.zeros_like(attention_mask)
    result_zero = embedder._mean_pooling(model_output, attention_mask_zero)
    assert torch.allclose(result_zero, torch.zeros_like(result_zero))

test_mean_pooling()
