import json
import hashlib


class Block:
    def __init__(self, transactions, block_index, previous_hash, proof):
        self.block_index = block_index
        self.timestamp = time.time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def block_to_json(self):
        # transactions are objects so need another stage of dumping
        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.get_transaction_json())

        hashable_dict = {
            'block_index': self.block_index,
            'timestamp': self.timestamp,
            'transactions': json_transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }

        block_json = json.dumps(hashable_dict, sort_keys=True).encode()
        return block_json

    def hash_block(self):
        block_json = self.block_to_json()
        return hashlib.sha256(block_json).hexdigest()

    def __repr__(self):
        return '<Block %s : Previous hash: %s>' % (self.block_index, self.previous_hash)

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def mine_block(self):
        last_proof = self.proof
        last_hash = self.previous_hash

        # Simple proof of work algorithm
        proof = 0
        while not self.valid_proof(last_proof, proof, last_hash):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
