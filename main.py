"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from spagbol import Spagbol
from spagbol.loading import AlpacaLoader
from spagbol.reduction import PcaReduction
from spagbol.embedding import AllMiniLMEmbedder
from spagbol.clustering import GaussianMixtureClustering
from spagbol.similarity import CosineSimilarity
from spagbol import configure

import json
from flask_injector import FlaskInjector
from flask import Flask

app = Flask(__name__)
FlaskInjector(app=app, modules=[configure])

data_loader = AlpacaLoader("tatsu-lab/alpaca")
reducer = PcaReduction()
embedder = AllMiniLMEmbedder()
clustering = GaussianMixtureClustering()
similarity_measure = CosineSimilarity()


module = Spagbol(data_loader=data_loader, embedder=embedder,
                 clustering_model=clustering, reducer=reducer)

module.load_data()
