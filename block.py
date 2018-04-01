import json
import hashlib


class Block:
    def __init__(self, transactions, block_index, previous_hash, timestamp):
        self.block_index = block_index
        self.timestamp = timestamp
        self.transactions = transactions

        self.previous_hash = previous_hash

        self.__proof = None
        self.__block_hash = None
        self.hash_block()

    def block_to_json(self):
        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.get_transaction_json())

        hashable_dict = {
            'block_index': self.block_index,
            'timestamp': self.timestamp,
            'transactions': json_transactions,
            'previous_hash': self.previous_hash
        }

        block_json = json.dumps(hashable_dict, sort_keys=True).encode()
        return block_json

    def hash_block(self):
        block_json = self.block_to_json()
        self.block_hash = hashlib.sha256(block_json).hexdigest()

    def __repr__(self):
        return '<Block %s : Previous hash: %s>' % (self.block_index, self.previous_hash)

    @staticmethod
    def valid_proof(proof, last_hash):
        guess = f'{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def mine_block(self):
        last_hash = self.previous_hash

        # Simple proof of work algorithm
        proof = 0
        while not self.valid_proof(proof, last_hash):
            proof += 1

        self.proof = proof
        return proof

    @property
    def proof(self):
        return self.__proof

    @proof.setter
    def proof(self, proof):
        self.__proof = proof

    @property
    def block_hash(self):
        return self.__block_hash

    @block_hash.setter
    def block_hash(self, block_hash):
        self.__block_hash = block_hash
