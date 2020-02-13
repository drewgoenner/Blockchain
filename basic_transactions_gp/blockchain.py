# Paste your version of blockchain.py from the client_mining_p
# folder here
import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash="I'm a teapot", proof=100)
    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block
    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block": <dict> Block
        "return": <str>
        """
        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1
    @property
    def last_block(self):
        return self.chain[-1]
    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     # TODO
    #     block_string = json.dumps(block, sort_keys=True)
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         proof += 1

    #     return proof
        # return proof
    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] == "000000"
        # return True or False
# Instantiate our Node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
blockchain = Blockchain()
print(blockchain.chain)
print(blockchain.hash(blockchain.last_block))
@app.route('/mine', methods=['POST'])
def mine():
   #check if the block is valid
    data = request.get_json()
    required = ['proof', 'id']

    for key in required:
        if key not in data:
        	response = {
        	'Error': 'Required data not present'
        	}
        code = 400
    #check if proof is valid
    else:
        block_string = json.dumps(blockchain.last_block, sort_keys = True)

        miner_proof = data['proof']
        miner_id = data['id']

        if blockchain.valid_proof(block_string, miner_proof):
            previous_hash = blockchain.hash(blockchain.last_block)
            blockchain.new_transaction('0', miner_id, 1)
            new_block = blockchain.new_block(miner_proof, previous_hash)
            response = {
            'status': 'success',
            'message': 'New Block Forged',
            'block': new_block
            }
            code = 200
        else:
            response = {
            'status': 'failure',
            'message': 'please try again',
            'block': blockchain.last_block
            }
            code = 400

    return jsonify(response), code

@app.route('/transactions/new', methods=['POST'])
def transact():
    data = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if required:
        response = {
            'message': f'transaction added to   block {index}'
        }
        return jsonify(response), 200
    else:
        response = {
            'message:' 'ERROR: Data Missing'
        }
        return jsonify(response), 400

@app.route('/last_block', methods=['GET'])
def get_last():
	response = {
	'block': blockchain.chain[-1]
	}
	return jsonify(response), 200
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200
# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
