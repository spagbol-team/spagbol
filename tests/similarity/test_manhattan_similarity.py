import numpy as np

from spaghetti.similarity import ManhattanSimilarity


def test_single_similarity():
    x = np.ones([384])
    y = np.ones([384])

    assert (abs(ManhattanSimilarity.compute(x, y)) == 0)


def test_batched_similarity():
    x = np.ones([384])
    y = np.ones([40, 384])

    similarities = ManhattanSimilarity.compute_batch(x, y)
    for sim in similarities:
        assert abs(sim) == 0
