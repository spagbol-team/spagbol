"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
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
