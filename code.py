import hashlib
import json
import time
from flask import Flask, request

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = f'{index}{previous_hash}{timestamp}{data}'
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

blockchain = [create_genesis_block()]

app = Flask(__name__)

@app.route('/blocks', methods=['GET'])
def get_blocks():
    return json.dumps([block.__dict__ for block in blockchain])

@app.route('/mine_block', methods=['POST'])
def mine_block():
    data = request.json['data']
    previous_block = blockchain[-1]
    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)
    return json.dumps(new_block.__dict__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)