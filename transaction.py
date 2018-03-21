

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f'Sender: {self.sender} Recipient: {self.recipient} Amount: {self.amount}'
