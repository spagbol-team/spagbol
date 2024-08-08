from typing import Dict, Any
import os
import json
import numpy as np
from typing import List, Optional

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
        self.write_mode = False

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
            print(self.current_partition, self.save_path)
            with open(path_to_partition, "r") as fs:
                self.cache = json.load(fs)
                self.current_partition_size = len(self.cache)

    def save_partition(self):
        if self.current_partition is None:
            return
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        with open(os.path.join(self.save_path, self.current_partition), "w") as fs:
            json.dump(self.cache, fs, indent=4)
        self.partition_map.save(self.save_path)

    def get(self, entry_id: str):
        partition_id = self.partition_map.find_partition(entry_id)
        if partition_id is None:
            return None
        if partition_id != self.current_partition:
            if self.write_mode:
                self.save_partition()
            self.current_partition = partition_id
            self.load_partition()
        return self.cache.get(str(entry_id))

    def get_batch(self, entry_ids: List[str]) -> List[Optional[Any]]:
        output = []
        for entry_id in entry_ids:
            output.append(self.get(entry_id))
        return output

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
            ids_batch = []
            for entry_id, datapoint in self.cache.items():
                batch.append(datapoint)
                ids_batch.append(entry_id)
                if len(batch) >= batch_size:
                    yield ids_batch, batch
                    batch = []
                    ids_batch = []
            if len(batch) != 0:
                yield ids_batch, batch

    def propagate_partition(self):
        if self.write_mode:
            self.save_partition()
        self.partition_map.propagate_partition()
        self.current_partition = self.partition_map.current_partition
        self.load_partition()

    def add_data(self, data: Dict[str, Any]) -> None:
        self.write_mode = True
        last_partition_id = self.partition_map.get_last_partition()
        if last_partition_id is not None:
            if last_partition_id != self.current_partition:
                self.current_partition = last_partition_id
                self.load_partition()
                self.partition_map.set_current_partition(last_partition_id)
        else:
            self.propagate_partition()

        for entry_id, datapoint in data.items():
            while self.current_partition_size >= self.partition_size:
                self.propagate_partition()
            existing_partition = self.partition_map.find_partition(entry_id)
            if existing_partition is not None:
                self.current_partition = existing_partition
                self.load_partition()
            self.cache[entry_id] = datapoint
            if existing_partition is None:
                self.current_partition_size += 1
                self.partition_map.add(entry_id)
        if self.current_partition_size >= self.partition_size:
            self.propagate_partition()

        self.write_mode = False

    def delete_data(self, data: Dict[str, Any]) -> None:
        for entry_id, data_point in data.items():
            entry = self.get(str(entry_id))
            if entry is not None:
                del self.cache[str(entry_id)]
                self.partition_map.map[self.current_partition].remove(str(entry_id))
        self.save_partition()

    def group_ids_by_partition(self, ids):
        ids_by_partition = {}
        for entry_id in ids:
            partition_name = self.partition_map.find_partition(entry_id)
            if partition_name not in ids_by_partition:
                ids_by_partition[partition_name] = []
            ids_by_partition[partition_name].append(entry_id)
        return ids_by_partition
