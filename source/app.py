from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/mine', methods=['GET'])
def mine():


    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)


    blockchain.new_transaction(
        sender=0,
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Forged new block.",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response, 200)

@app.route('/transaction/new', methods=['GET'])
def new_transaction():

    values = request.get_json()
    required = ['sender', 'recipient', 'amont']

    if not all(k in values for k in required):
        return 'Missing values.', 400

    index = blockchain.new_transaction(
        sender = values['sender'],
        recipient = values['recipient'],
        amount = values['amount']
    )

    response = {
        'message': f'Transaction will be added to the Block {index}',
    }
    return jsonify(response, 200)

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    print('values',values)
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes: blockchain.register_node(node)

    response = {
        'message': "New nodes have been added",
        'all_nodes': list(blockchain.nodes),
    }

    return jsonify(response), 201