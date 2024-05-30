import json
import os
from typing import Dict, List, Optional
from collections import defaultdict


class PartitionMap:
    def __init__(self):
        self.map = defaultdict(list)
        self.partition_counter = 0
        self.current_partition = None
        self.partition_index = 0

    def add(self, entry_id: str):
        if self.current_partition is None and self.partition_counter == 0:
            self.propagate_partition()
        self.map[self.current_partition].append(entry_id)

    def add_batch(self, batch: List[str]):
        if self.current_partition is None and self.partition_counter == 0:
            self.propagate_partition()
        self.map[self.current_partition] += batch

    def propagate_partition(self):
        self.partition_index += 1
        partition_names = list(self.map.keys())
        if len(partition_names) > self.partition_index:
            self.current_partition = partition_names[self.partition_index]
        else:
            self.partition_counter += 1
            self.current_partition = "partition_%s" % self.partition_counter

    def load(self, path_to_map: str):
        path_to_map = os.path.join(path_to_map, "partition_map.json")
        if not os.path.exists(path_to_map) or not os.path.exists(path_to_map):
            return False
        with open(path_to_map, "r") as fs:
            self.map = json.load(fs)
        self.partition_counter = len(self.map)
        last_partition_name = list(self.map.keys())[-1]
        self.current_partition = last_partition_name
        return True

    def save(self, save_path: str):
        path_to_map = os.path.join(save_path, "partition_map.json")
        with open(path_to_map, "w") as fs:
            json.dump(self.map, fs, indent=4)

    def set_current_partition(self, partition_name: str):
        self.current_partition = partition_name
        if partition_name not in self.map:
            self.partition_counter += 1
            self.partition_index += self.partition_counter
        else:
            self.partition_index = list(self.map.keys()).index(partition_name)

    def find_partition(self, entry_id: str) -> Optional[str]:
        for partition_name, entries in self.map.items():
            if entry_id in entries:
                return partition_name
        return None

    def get_last_partition(self) -> Optional[str]:
        if len(self.map) > 0:
            return list(self.map.keys())[-1]
        return None
