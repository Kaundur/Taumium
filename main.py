
import flask
import blockChain

import transaction


app = flask.Flask(__name__)

blockchain = blockChain.BlockChain()

# Note, here we host both the wallet and server, this should be separate otherwise
# we will compromise our private key on transaction

@app.route('/')
def index():
    return '(τ) Taumium'


@app.route('/wallet/send')
def wallet_send():
    return flask.render_template('send_taumium.html')


@app.route('/mine')
def mine():
    # This should be set by the miner
    hardcoded_mining_address = 99
    blockchain.mine(hardcoded_mining_address)
    return 'Block successfully mined'


@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    # Note - private keys should never be sent to a server. However, in this demo it is convenient to host the wallet
    # and node in the same place

    values = flask.request.form
    # Check the values are in the post data
    required = ['sender', 'recipient', 'amount', 'private_key']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # sign_transaction(values['private_key'])
    t = transaction.Transaction(values['sender'], values['recipient'], values['amount'])
    t.sign_transaction(values['private_key'])

    block_added = blockchain.add_transaction(t)
    if block_added:
        response = {'message': 'Transaction has been added to the minable transaction list'}
        return flask.jsonify(response), 201

    response = {'message': 'Invalid public private key combination'}
    return flask.jsonify(response), 201


@app.route('/transaction/total')
def total_amount():
    return str(blockchain.total_amount())


@app.route('/transaction/pending')
def transactions_pending():
    return flask.render_template('pending_transactions.html', pending_transactions=blockchain.pending_transactions())


@app.route('/blockchain/validate')
def validate_chain():
    is_valid = blockchain.validate_chain(blockchain.chain)

    return str(is_valid)


@app.route('/blockchain/history')
def blockchain_history():
    return flask.render_template('blockchain_history.html', blocks=blockchain.chain)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
