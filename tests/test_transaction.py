import unittest

from main import app

test_app = app.test_client()


class TestTransaction(unittest.TestCase):
    def test_send(self):
        res = test_app.post('transaction/new', data=dict(sender=0, recipient=1, amount=2))
        res = test_app.post('transaction/new', data=dict(sender=0, recipient=1, amount=2))
        self.assertEqual(res._status_code, 201)

        res = test_app.get('transaction/pending')
        print(res)
