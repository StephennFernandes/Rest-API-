import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items=[]

class Item(Resource):

    #putting parser as class item , so no need to re-write it for all endpointsthat will need parser 
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, required=True,                      # constrainting users to not change specific params
        help="this field cant be left blank"
        )



    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)   # used code from @classmethod below and used it here 
        if item:
            return item 
        return {'message':'item not found'}, 404

        @classmethod
        def find_by_name(cls, name):
            connection = sqlite3.connect('data.db')
            cursor=connection.cursor()

            query = "SELECT * FROM items WHERE name=?"
            result = cursor.execute(query, (name,))
            row = result.fetchone()
            connection.close()

            if row:
                return {'item':{'name': row[0], 'price': row[1]}}

    def post(self, name):

        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400   # using classmehtod code 



        data = Item.parser.parse_args()    # replaces get_json()
       # data = request.get_json(force=True)   # force means its ok if theres no content-type header , silent = True (returns none if noe content type header )
        item = {'name':name, 'price':data['price']}
        
        try:
            self.insert(item)
        except:
            return {"message":"An Error occurred , inserting item"}, 500    # internal server error 
        return item, 201
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO itmes VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

    def delete(self, name):
        connection= sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))                      
        
        connection.commit()
        connection.close()

        return {'message':'Item Deleted'}

    def put(self, name):
       
        data = Item.parser.parse_args()
    
        item = self.find_by_name(name)
        updated_item = {'name':name, 'price':data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message":"an error occured inserting the item "}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message":"an error occured updating the item"}, 500
        return updated_item
    
    @classmethod 
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE itmes SET price=? wHERE name=?"
        cursor.execute(query, (item['price'],item['name']))
        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})

        connection.close()
        return {'items':items}        