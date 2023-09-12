import numpy as np

from spaghetti.reduction import PcaReduction
from spaghetti.errors import UnfitModelError


def test_fit_transform():
    x = np.random.rand(350, 384)
    reducer = PcaReduction()
    reduced_data = reducer.fit_transform(x)
    assert reduced_data.shape[1] == 2
    assert reduced_data.shape[0] == x.shape[0]


def test_transform():
    x = np.random.rand(350, 384)
    reducer = PcaReduction()
    try:
        reducer.transform(x)
    except UnfitModelError:
        reducer.fit(x)
        reduced_data = reducer.transform(x)
        assert reduced_data.shape[1] == 2
        assert reduced_data.shape[0] == x.shape[0]
        return

    # If it didn't throw the exception, fail the test.
    assert False
