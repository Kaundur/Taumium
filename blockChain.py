import block


class BlockChain:
    def __init__(self):
        self.chain = []
        self.transactions = []

        # Create genesis block
        self.new_block(0, '')

    def last_block(self):
        return self.chain[-1]

    def new_block(self, block_index, previous_hash):
        self.chain.append(block.Block(self.transactions, block_index, previous_hash))
        self.transactions = []

        print('New block created')
        print(self.last_block())

    def add_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return len(self.chain)

    def total_amount(self):
        amount = 0
        for t in self.transactions:
            amount += int(t['amount'])

        return amount
