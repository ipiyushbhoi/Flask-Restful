from flask import Flask, jsonify, request

app = Flask(__name__)


# HTTPS Verbs - [GET, POST, PUT, DELETE]
# For Server:
#     POST - used to receive data
#     GET - used to send data back only
# For Browser:
#     GET - used to receive data
#     POST - used to send data

stores = [
    {
        "name": "Store1",
        "items": [
            {
                "name": "Iphone",
                "price": "75000"
            }
        ]
    }
]

# POST /store data: {name: }
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET  /store/<string:name>
@app.route('/store/<string:name>') # http://127.0.0.1:5000/store/some_name
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return ({'message': "Store not Found"})

# GET  /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return ({'message': "Store not Found"})

# GET  /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'itmes': store['items']})
    return jsonify({'message': 'Item not found'})

@app.route('/') # http://www.google.com/'
def home():
    return "Hello World.."

app.run(port=5000)
