"""
Copyright 2023 [name of copyright owner]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

import pandas as pd
from pandas.errors import ParserError
from urllib.error import HTTPError
from validators import url as is_valid_url
import os
from datasets import load_dataset

from spaghetti.loading.DataLoader import DataLoader
from spaghetti.errors import InvalidSourceError


class AlpacaLoader(DataLoader):
    """
    Data loader for Alpaca dataset. Supports both base and clean version of the dataset.
    You can load the dataset from file with load_dataset method,
    url or Huggigface Hub, for file and URL only CSV is supported.
    Example usages:
        For local csv file:
            loader = AlpacaLoader(source="/path/to/alpaca.csv")
            dataset = loader.load_data()
        For remote csv:
            loader = AlpacaLoader(source="https://url/to/alpaca.csv")
            dataset = loader.load_data()
        For Huggigface Hub:
            loader = AlpacaLoader(source="tatsu-lab/alpaca") # Or you can use any other alpaca from the hub
            dataset = loader.load_data(split=preferred_dataset_part) # 'train' is used as a default split value

    :param source: Source of the dataset. Supported sources: URL, absolute path and huggingface hub.
    """

    def __init__(self, source: str):
        self.source = source

    def load_data(self, split=None) -> pd.DataFrame:
        """
        Loads dataset from the source.
        :param split: Optional parameter for loading from Hugginface Hub to select a part of dataset to load.
                      'train' is selected by default.
        :return: Loaded and converted dataset. You can see conversion process in _convert_dataset method.
        :raises InvalidSourceError:
        """
        if is_valid_url(self.source):
            try:
                dataset = pd.read_csv(self.source)
            except ParserError:
                raise InvalidSourceError("Couldn't parse file from path or URL. Maybe it has a wrong format.")
            except HTTPError:
                raise InvalidSourceError(
                    "Couldn't reach this source URL, it may have a protected access or is inactive."
                )
        elif os.path.exists(self.source):
            try:
                dataset = pd.read_csv(self.source)
            except ParserError:
                raise InvalidSourceError("Couldn't parse file from path or URL. Maybe it has a wrong format.")
            except UnicodeDecodeError:
                raise InvalidSourceError(
                    "Encountered UnicodeDecode error while parsing the file. Maybe it has a wrong format."
                )
        else:
            try:
                dataset_split = "train"
                if split is not None:
                    dataset_split = split
                huggingface_dataset = load_dataset(self.source, split=split)
                dataset = pd.DataFrame(huggingface_dataset[dataset_split])
            except FileNotFoundError:
                raise InvalidSourceError("Source is not a valid url, path or huggingface hub dataset")
            except ValueError as e:
                raise InvalidSourceError(e.__str__())

        return self._convert_dataset(dataset)

    def _convert_dataset(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Converts Alpaca dataset to our universal format.

        :param dataset: Raw Alpaca dataset
        :return: Converted dataset
        """
        output_dataset = pd.DataFrame()
        output_dataset["input"] = dataset["instruction"] + " " + dataset["input"]
        output_dataset["input"] = output_dataset["input"].apply(lambda x: x.strip())
        output_dataset["output"] = dataset["output"]
        return output_dataset
