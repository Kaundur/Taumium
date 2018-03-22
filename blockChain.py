import block
import transaction


class BlockChain:
    def __init__(self):
        self.chain = []
        self.transactions = []

        # Create genesis block
        self.new_block(0, '999', 999)

    def last_block(self):
        return self.chain[-1]

    def new_block(self, block_index, previous_hash, proof):
        self.chain.append(block.Block(self.transactions, block_index, previous_hash, proof))
        self.transactions = []

        print('New block created')
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

    def mine_latest_block(self):

        latest_block = self.last_block()

        # Mine the current block
        proof = latest_block.mine_block()

        # Send mining reward to the miner
        mining_reward_amount = self.calculate_mining_reward_amount()

        # Hardcode sender and recipient for now
        sender = 0
        recipient = 0

        self.add_transaction(sender, recipient, mining_reward_amount)

        # Get the hash of the current block
        previous_block_hash = latest_block.hash_block()

        # Create the new block
        self.new_block(len(self.chain), previous_block_hash, proof)

    def calculate_mining_reward_amount(self):
        # For now return 1, later this should scale to the size of the chain
        return 1