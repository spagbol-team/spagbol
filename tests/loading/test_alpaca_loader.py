"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import pandas as pd
from datasets import load_dataset
import os
import numpy as np

from spagbol.loading.AlpacaLoader import AlpacaLoader


def _load_temp_alpaca():
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    if not os.path.exists("tmp/tmp_alpaca.csv"):
        dataset = load_dataset("tatsu-lab/alpaca")
        df = pd.DataFrame(dataset["train"])
        df = df.replace(np.nan, "")
        df.to_csv("tmp/tmp_alpaca.csv", index=False)


def test_url_loader():
    loader = AlpacaLoader("https://raw.githubusercontent.com/gururise/AlpacaDataCleaned/main/alpaca_data_cleaned.json")
    dataset = loader.load_data()
    assert "input" in dataset.columns
    assert "text" not in dataset.columns
    assert "output" in dataset.columns
    assert len(dataset) == 51760


def test_local_loader():
    _load_temp_alpaca()
    loader = AlpacaLoader("tmp/tmp_alpaca.csv")
    dataset = loader.load_data()
    assert "input" in dataset.columns
    assert "text" not in dataset.columns
    assert "output" in dataset.columns
    assert len(dataset) == 52002


def test_huggingface_loader():
    loader = AlpacaLoader("tatsu-lab/alpaca")
    dataset = loader.load_data()
    assert "input" in dataset.columns
    assert "text" not in dataset.columns
    assert "output" in dataset.columns
    assert len(dataset) == 52002
