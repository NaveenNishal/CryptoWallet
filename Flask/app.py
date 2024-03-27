from flask import Flask, jsonify, request, render_template
from hashlib import sha256
import json
import uuid
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Define the Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0

    def calculate_hash(self):
        block_str = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_str.encode()).hexdigest()

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "01/01/2022", "Genesis Block", "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

# Define the Wallet class
class Wallet:
    def __init__(self):
        self.address = generate_wallet_address()
        self.balance = 1000

# Generate a unique wallet address
def generate_wallet_address():
    return str(uuid.uuid4()).replace("-", "")

# Initialize the blockchain and transaction history
blockchain = Blockchain()

# API endpoint for checking wallet balance
@app.route('/balance', methods=['GET'])
def get_balance():
    response = {
        'address': wallet.address,
        'balance': wallet.balance
    }
    return jsonify(response), 200

# API endpoint for making transactions
@app.route('/transaction', methods=['POST'])
def make_transaction():
    global transaction_history  # Access the global transaction history list
    data = request.get_json()
    recipient_address = data['recipient']
    amount = data['amount']

    if wallet.balance < amount:
        return jsonify({'message': 'Insufficient balance!'}), 400

    # Update wallet balance
    wallet.balance -= amount

    # Add transaction to the transaction history
    transaction = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'sender_address': wallet.address,
        'recipient_address': recipient_address,
        'amount': amount
    }
    transaction_history.append(transaction)

    response = {
        'message': 'Transaction successful!',
        'sender_address': wallet.address,
        'recipient_address': recipient_address,
        'amount': amount
    }
    return jsonify(response), 200

# Serve the index.html file at the root URL
@app.route('/')
def index():
    return render_template('index.html')

# Serve the transaction_history.html file at the /transaction_history URL
@app.route('/transaction_history')
def transaction_history_page():
    return render_template('transaction_history.html', transactions=transaction_history)

if __name__ == '__main__':
    # Generate a new wallet and clear transaction history for every run
    wallet = Wallet()
    transaction_history = []
    app.run(debug=True)