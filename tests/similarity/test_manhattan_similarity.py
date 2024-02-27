"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np

from spagbol.similarity import ManhattanSimilarity


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
