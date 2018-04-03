import block
import transaction

import time


class BlockChain:
    MAX_TRANSACTIONS_PER_BLOCK = 2

    def __init__(self):
        self.chain = []
        self.transactions = []

        # Create genesis block
        self.create_genesis_block()
        # self.new_block(0, '999', 999)

    def create_genesis_block(self):
        # Sender, recipient, amount
        # Should change the recipient to a real hash once we have the key generation sorted
        first_genesis_transaction = transaction.Transaction(0, 1, 1000)
        second_genesis_transaction = transaction.Transaction(0, 2, 1000)

        genesis_transactions = [first_genesis_transaction, second_genesis_transaction]

        # transactions, block index, previous hash, timestamp
        genesis_block = block.Block(genesis_transactions, 0, "", time.time())
        self.add_block(genesis_block)

    def last_block(self):
        return self.chain[-1]

    def add_block(self, unvalidated_block):
        # should validate block here before adding
        self.chain.append(unvalidated_block)
        print('Unvalidated block added to chain')
        print(self.last_block())

    def add_transaction(self, sender, recipient, amount):
        self.transactions.append(transaction.Transaction(sender, recipient, amount))
        return len(self.chain)

    def total_amount(self):
        amount = 0
        for t in self.transactions:
            amount += int(t['amount'])

        return amount

    def pending_transactions(self):
        return self.transactions

    def get_next_unconfirmed_transaction(self):
        if len(self.transactions) > 0:
            return self.transactions.pop(0)
        return None

    def mine(self, mining_reward_address):

        # Generate a list of transactions to be mined
        mineable_transactions = []
        for i in range(self.MAX_TRANSACTIONS_PER_BLOCK):
            unconfirmed_transaction = self.get_next_unconfirmed_transaction()
            if unconfirmed_transaction is None:
                break

            mineable_transactions.append(unconfirmed_transaction)

        latest_block = self.last_block()

        # Calculate the reward amount for mining the block
        mining_reward_amount = self.calculate_mining_reward_amount()

        # Hardcode sender for now
        sender = 0

        # Add the mining reward to the block transactions
        mineable_transactions.append(transaction.Transaction(sender, mining_reward_address, mining_reward_amount))

        # Get the hash of the current block
        previous_block_hash = latest_block.block_hash

        block_index = latest_block.block_index + 1

        # Create the new block
        new_block = block.Block(mineable_transactions, block_index, previous_block_hash, time.time())

        # Now mine the new block
        # TODO - Here we need to monitor the chain to see if someone has beat us to a solution.
        # TODO - In this case we need to stop mining and start with a new block with a fresh list of transactions
        new_block.mine_block()

        # Once the block is mined, append it to the chain
        self.chain.append(new_block)

    def calculate_mining_reward_amount(self):
        # For now return 1, later this should scale to the size of the chain
        return 1

    @staticmethod
    def validate_chain(chain):
        last_block = chain[0]
        for _block in chain[1:]:
            if _block.previous_hash != last_block.hash_block():
                return False

            if not _block.valid_proof(last_block.proof, _block.proof, last_block.previous_hash):
                return False

            last_block = _block

        return True
