from injector import Module, provider, singleton
from spagbol.loading import DataLoader, AlpacaLoader
from spagbol.embedding import Embedder, AllMiniLMEmbedder
from spagbol.clustering import ClusteringModel, GaussianMixtureClustering
from spagbol.reduction import DimensionalityReduction, PcaReduction
from spagbol import Spagbol


class AppModule(Module):
    def __init__(self, source=None):
        self.source = source

    @singleton
    @provider
    def provide_data_loader(self) -> DataLoader:
        return AlpacaLoader(source=self.source)

    @singleton
    @provider
    def provide_embedder(self) -> Embedder:
        return AllMiniLMEmbedder()

    @singleton
    @provider
    def provide_clustering_model(self) -> ClusteringModel:
        return GaussianMixtureClustering()

    @singleton
    @provider
    def provide_reducer(self) -> DimensionalityReduction:
        return PcaReduction()

    @singleton
    @provider
    def provide_spagbol(self, data_loader: DataLoader, embedder: Embedder,
                        clustering_model: ClusteringModel, reducer: DimensionalityReduction) -> Spagbol:
        return Spagbol(data_loader, embedder, clustering_model, reducer)