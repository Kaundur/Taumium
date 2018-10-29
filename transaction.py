import json
import ecdsa


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def __repr__(self):
        return f'Sender: {self.sender} Recipient: {self.recipient} Amount: {self.amount} Signature: {self.signature}'

    def get_base_transaction(self):
        base_transaction = {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }
        return base_transaction

    def get_transaction_json(self):
        hashable_dict = self.get_base_transaction()
        # Add the signature to the block so it can be verified in the future
        hashable_dict['signature'] = self.signature

        return json.dumps(hashable_dict, sort_keys=True)

    def sign_transaction(self, private_key_string):
        hashable_dict = self.get_base_transaction()

        transaction_string = json.dumps(hashable_dict, sort_keys=True).encode('utf-8')

        private_key = self.get_private_key_from_string(private_key_string)
        if private_key:
            self.signature = private_key.sign(transaction_string).hex()

    def get_private_key_from_string(self, hex_string):
        try:
            bytes_string = bytes.fromhex(hex_string)
            return ecdsa.SigningKey.from_string(bytes_string, curve=ecdsa.SECP256k1)
        except AssertionError:
            return None

    def get_public_key_from_string(self, public_key_string):
        try:
            bytes_string = bytes.fromhex(public_key_string)
            return ecdsa.VerifyingKey.from_string(bytes_string, curve=ecdsa.SECP256k1)
        except AssertionError:
            return None

    def is_valid(self):
        # If there is no signature the transaction is not valid
        if not self.signature:
            return False

        hashable_dict = self.get_base_transaction()
        transaction_string = json.dumps(hashable_dict, sort_keys=True).encode('utf-8')

        public_key = self.get_public_key_from_string(self.sender)

        # If the public key cannot be formed then the transaction cannot be valid
        if not public_key:
            return False

        signature = bytes.fromhex(self.signature)
        return public_key.verify(signature, transaction_string)
