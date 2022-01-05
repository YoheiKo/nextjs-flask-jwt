from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
CORS(app)
app.secret_key = 'Ryosei'
api = Api(app)

# Create a JWT object
# JWT extension creates an /auth endpoint and return a jwt token
# the user use the token for request and JWT check if it is valid by the identity function
jwt = JWT(app, authenticate, identity) 

# This list will contain dictionaries of each item 
items = []

# define the resource for each item
class Item(Resource):
    @jwt_required() #need to be authenticated befor GET
    def get(self,name): # define the method
        # IF the next does not find a match it will return None
        item = next(filter(lambda item: item['name'] == name, items), None)
        # for item in items:
        #    if item['name'] == name:
                #return item # flask restful does jsonify for us. We can just return dictinary

        return item, 200 if item else 404
        # python returns "None" by default, but the return should be a dictionary to be understoord by the frontend
        # This is a valid return and will return status 200, which means everything is OK and I give you what you wanted. But it should be 404.
        return {'item': None}, 404 
    
    def post(self,name):
        if next(filter(lambda item: item['name'] == name, items), None): #If the item exists
            return {'message': "An item witn the name '{}' already exits".format(name)}, 400 #Bad request
        #"request" imported from flask has the JSON payload Body attached to it upon each request
        # This will give you an error if the request does not have a valid Header or JSON body
        data = request.get_json() #"force=True" sets the content-type by reading the body. silent=True give you a None instead of an error
        item = {'name': name, 'price': data['price']} # this name parameter comes from the <string:name>
        items.append(item)
        return item, 201 # return the item so that the app know the this has happens. 201 is for CREATED     

# define another resourece for items
class ItemsList(Resource):
    def get(self):
        return {'items': items}, 200

# add the resoureces and give the endpoints
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True)