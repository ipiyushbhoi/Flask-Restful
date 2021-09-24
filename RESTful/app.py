from security import authenticate, identity
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'some-hash'
api = Api(app)
jwt = JWT(app, authenticate, identity) # /auth

# In-memory database: It will get destroyed, if application is stopped
items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['item'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['item'] == name, items), None) is not None:
            return {'message': 'An item with name {} already exists'.format(name)}, 400

        request_data = request.get_json()
        item = {'item': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        try:
            global items
            items = list(filter(lambda x: x['item'] != name, items))
            return {"message": "item is deleted"}, 200
        except Exception as exp:
            return {"message": str(exp)}, 400

    def put(self, name):
        request_data = request.get_json()
        item = next(filter(lambda x: x['item'] == name, items), None)
        if item is None:
            item = {'item': name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)

class Itemlist(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:5000/item/mobile
api.add_resource(Itemlist, '/items') #http://127.0.0.1:5000/items

app.run(port=5000, debug=True)
