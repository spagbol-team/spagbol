"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


class NoDatasetError(Exception):
    """
    Error class for Spagbol module that indicates that dataset was not loaded
    """
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class ClusteringError(Exception):
    """
    Error for clustering operation is Spagbol module
    """
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg