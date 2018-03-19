import flask

import blockChain

app = flask.Flask(__name__)

blockchain = blockChain.BlockChain()

@app.route('/')
def index():
    return '(τ) Taumium'

@app.route('/wallet/send')
def wallet_send():
    return flask.send_from_directory('wallet', 'send.html')

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = flask.request.form

    # Check the values are in the post data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    block_index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to <Block %s>' % block_index}
    return flask.jsonify(response), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
