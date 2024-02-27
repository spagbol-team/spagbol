"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from abc import ABC, abstractmethod
import pandas as pd


class DataLoader(ABC):
    """
    This is the interface for all data loaders used in this project.
    Every data loder used with other parts of the project has to implement this interface

    :param source: Source of the dataset, whether it is an url or path to the file
    """
    @abstractmethod
    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """
        This method has to load data based on the source, it has to work with all types of sources:
        URL, path, huggingface_hub. It has to convert loaded dataset into a universal format. See README.md
        Data Format section.
        :return: Loaded and converted dataset in pandas.DataFrame format
        """
        raise NotImplementedError()

    @abstractmethod
    def _convert_dataset(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Private method that should contain script that converts loaded dataset into the universal format
        See README.md Data Format section. Should be used inside the load_data method
        :param dataset: Dataset that needs to be converted
        :return: Converted version of the dataset in pandas.DataFrame format
        """
        raise NotImplementedError()
