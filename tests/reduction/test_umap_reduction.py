"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np

from spagbol.reduction import UmapReduction
from spagbol.errors import UnfitModelError


def test_fit_transform():
    x = np.random.rand(350, 384)
    reducer = UmapReduction()
    reduced_data = reducer.fit_transform(x)
    assert reduced_data.shape[1] == 2
    assert reduced_data.shape[0] == x.shape[0]


def test_transform():
    x = np.random.rand(350, 384)
    reducer = UmapReduction()
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
