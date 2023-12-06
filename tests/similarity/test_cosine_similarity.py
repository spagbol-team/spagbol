import numpy as np

from spagbol.similarity import CosineSimilarity


def test_single_similarity():
    x = np.ones([384])
    y = np.ones([384])

    assert (int(CosineSimilarity.compute(x, y)) == 1)


def test_batched_similarity():
    x = np.ones([384])
    y = np.ones([40, 384])

    similarities = CosineSimilarity.compute_batch(x, y)
    for sim in similarities:
        assert int(sim) == 1
