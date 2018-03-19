import time
import json
import hashlib


class Block:
    def __init__(self, transactions, block_index, previous_hash):
        self.block_index = block_index
        self.timestamp = time.time()
        self.transactions = transactions
        self.proof = None
        self.previous_hash = previous_hash
        self._hash = self.hash_block()

    def block_to_json(self):
        hashable_dict = {
            'block_index': self.block_index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }
        block_json = json.dumps(hashable_dict, sort_keys=True).encode()
        return block_json

    def hash_block(self):
        block_json = self.block_to_json()
        return hashlib.sha256(block_json).hexdigest()

    def __repr__(self):
        return '<Block %s> : %s' % (self.block_index, self._hash)
