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

    def test_total(self):
        # This is a hack to negate previous transactions resulting from previously run unit tests
        response = test_app.get('transaction/total')
        initial_result = int(str(response.data)[2:-1])
        # End hack

        res = test_app.post('transaction/new', data=dict(sender=0, recipient=1, amount=2))
        res = test_app.post('transaction/new', data=dict(sender=0, recipient=1, amount=3))
        response = test_app.get('transaction/total')
        result = int(str(response.data)[2:-1])
        self.assertEqual(response._status_code, 200)
        self.assertEqual(result - initial_result, 5)
