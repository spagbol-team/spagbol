from typing import Dict, Any
import os
import json
import numpy as np

from spagbol.partitioning import PartitionMap


class PartitionManager:
    def __init__(self, save_path: str, partition_size: int = 1000):
        self.save_path = ""
        self.partition_size = partition_size
        self.current_partition_size = 0
        self.cache = {}
        self.current_partition = None
        self.partition_map = PartitionMap()
        self.set_partition_path(save_path)

    def set_partition_path(self, partition_path):
        self.save_path = partition_path
        partition_exists = False
        if self.partition_map.load(partition_path):
            self.current_partition = self.partition_map.current_partition
            self.current_partition_size = len(self.partition_map.map[self.current_partition])
            self.load_partition()
            partition_exists = True
        return partition_exists

    def load_partition(self):
        path_to_partition = os.path.join(self.save_path, self.current_partition)
        if not os.path.exists(path_to_partition):
            self.cache = {}
            self.current_partition_size = 0
        else:
            with open(path_to_partition, "r") as fs:
                self.cache = json.load(fs)
                self.current_partition_size = len(self.cache)

    def save_partition(self):
        if self.current_partition is None:
            return
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        with open(os.path.join(self.save_path, self.current_partition), "w") as fs:
            json.dump(self.cache, fs)
        self.partition_map.save(self.save_path)

    def get(self, entry_id: str):
        partition_id = self.partition_map.find_partition(entry_id)
        if partition_id is None:
            return None
        if partition_id != self.current_partition:
            self.save_partition()
            self.current_partition = partition_id
            self.load_partition()
        return self.cache[str(entry_id)]

    def entries(self):
        for entry_id, datapoint in self.cache.items():
            yield entry_id, datapoint

    def batches(self, batch_size: int):
        batch = []
        for entry_id, datapoint in self.cache.items():
            if len(batch) >= batch_size:
                yield batch
                batch = []
            batch.append(datapoint)
        if len(batch) != 0:
            yield batch

    def partition_iterator(self):
        for partition, _ in self.partition_map.map.items():
            self.save_partition()
            self.partition_map.set_current_partition(partition)
            self.current_partition = self.partition_map.current_partition
            self.load_partition()
            for entry_id, datapoint in self.cache.items():
                yield entry_id, datapoint

    def batched_partition_iterator(self, batch_size):
        for partition, _ in self.partition_map.map.items():
            self.save_partition()
            self.partition_map.set_current_partition(partition)
            self.current_partition = self.partition_map.current_partition
            self.load_partition()
            batch = []
            for entry_id, datapoint in self.cache.items():
                batch.append(datapoint)
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            print(len(batch))
            if len(batch) != 0:
                yield batch

    def propagate_partition(self):
        self.save_partition()
        self.partition_map.propagate_partition()
        self.current_partition = self.partition_map.current_partition
        self.load_partition()

    def add_data(self, data: Dict[str, Any]) -> None:
        last_partition_id = self.partition_map.get_last_partition()
        if last_partition_id is not None:
            if last_partition_id != self.current_partition:
                self.current_partition = last_partition_id
                self.load_partition()
                self.partition_map.set_current_partition(last_partition_id)
        else:
            self.propagate_partition()

        for entry_id, datapoint in data.items():
            if self.current_partition_size >= self.partition_size:
                self.propagate_partition()
            self.cache[entry_id] = datapoint
            self.current_partition_size += 1
            self.partition_map.add(entry_id)
        if self.current_partition_size >= self.partition_size:
            self.propagate_partition()

