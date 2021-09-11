from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Every Resource has to be a class

# In-memory database: It will get destroyed, if application is stopped
items = []

class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['item'] == name, items), None)
        return {'item': None}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['item'] == name, items), None) is not None:
            return {'message': 'An item with name {} already exists'.format(name)}, 400

        request_data = request.get_json()
        item = {'item': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

class Itemlist(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/item/mobile
api.add_resource(Itemlist, '/items') #http://127.0.0.1:5000/items

app.run(port=5000, debug=True)
