"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
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
