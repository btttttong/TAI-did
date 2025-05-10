from dataclasses import dataclass
from typing import List, Any
import hashlib
import json
from time import time

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = json.dumps(self.transactions, sort_keys=True) + str(self.timestamp) + (self.previous_hash or '')
        return hashlib.sha256(data.encode('utf-8')).hexdigest()