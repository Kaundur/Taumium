from flask import Flask, jsonify, request

import blockChain


app = Flask(__name__)

blockchain = blockChain.BlockChain()

@app.route('/')
def index():
    return '(τ) Taumium'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
