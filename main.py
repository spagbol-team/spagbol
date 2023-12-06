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
