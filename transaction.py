import json


class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f'Sender: {self.sender} Recipient: {self.recipient} Amount: {self.amount}'

    def get_transaction_json(self):
        hashable_dict = {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

        return json.dumps(hashable_dict, sort_keys=True)
