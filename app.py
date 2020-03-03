from  flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from user import UserRegister
from security import authenticate, identity
from item import Item, ItemList

app = Flask(__name__)
app_secret_key = 'randomsecretkey'
api = Api(app)

jwt = JWT(app, authenticate , identity)  #jwt creates new endpoint /auth wich takes username and password 


api.add_resource(Item, '/item/<string:name>')  
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ =='__main__':
    app.run(port=5000, debug=True)

