import block
import transaction

import time


class BlockChain:
    MAX_TRANSACTIONS_PER_BLOCK = 2

    def __init__(self):
        self.chain = []
        self.transactions = []

        # Genesis public/private key
        self.GENESIS_PRIVATE_KEY = '5830bbebd544cbaddbe31c49d3523a73fee1e0a87af947a5ad9b975e475ae7ca'
        self.GENESIS_PUBLIC_KEY = '74b2308becf58ac369ee3151a00a507eb7053cd13211a827304fd6e42239a89e2db0630ab2deea6a1b8c9f41f19c2e608df999b4b8731844e0b59d4e283bde55'

        # Address for the first transaction within the genesis block
        self.GENESIS_RECEIVER_PRIVATE_KEY = 'ce994e2a58ace792bcd84eb63f95ddb98f4d847f84cd28c788a9cdf40d01fd06'
        self.GENESIS_RECEIVER_PUBLIC_KEY = '579606838945e81e2baba18df15c5d528c351264ff1c21c9e758af1d21f46db29fb412f5a47ed362b22718da1b33602c830846d98da2a6731467bc82b2eefa91'

        # Address for where the mining reward is sent from
        self.MINING_REWARD_PRIVATE_KEY = '5d053da3afeb03ae870fffe768c3021f1ca991ed1f2a3b284408551447351d57'
        self.MINING_REWARD_PUBLIC_KEY = 'b0a552176531384a06105dfd6b3d137ccd283abe2f128bc32eb552bff45994bf9ab0767fc4d9cc463d47a1f28b00c4a36483f6f7add021e3313302779d0e63c4'

        # Create genesis block receiver
        self.create_genesis_block()

    def create_genesis_block(self):
        # Sender, recipient, amount
        # Should change the recipient to a real hash once we have the key generation sorted
        first_genesis_transaction = transaction.Transaction(self.GENESIS_PUBLIC_KEY, self.GENESIS_RECEIVER_PUBLIC_KEY, 1000)
        first_genesis_transaction.sign_transaction(self.GENESIS_PRIVATE_KEY)
        second_genesis_transaction = transaction.Transaction(self.GENESIS_PUBLIC_KEY, self.GENESIS_RECEIVER_PUBLIC_KEY, 1000)
        second_genesis_transaction.sign_transaction(self.GENESIS_PRIVATE_KEY)

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

    def add_transaction(self, transaction_obj):
        # Only add the transaction if its digital signature is valid
        if transaction_obj.is_valid():
            self.transactions.append(transaction_obj)
            return True
        return False

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

        # Add the mining reward to the block transactions
        mining_reward_transaction = transaction.Transaction(self.MINING_REWARD_PUBLIC_KEY, mining_reward_address, mining_reward_amount)
        mining_reward_transaction.sign_transaction(self.MINING_REWARD_PRIVATE_KEY)

        # mining_reward_transaction.sign_transaction()
        mineable_transactions.append(mining_reward_transaction)

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
