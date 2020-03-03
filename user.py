import sqlite3 
from flask_restful import Resource, reqparse

class User:
    def __init__(self , _id , username, password):
        self.id = _id
        self.username = username 
        self.password = password
        
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # the only way to use parameters is to make it as a tuple (,) -> is used to maintain the tuple 
        row = result.fetchone()
        if row: 
            user = cls(*row) # makes a user object form class USER ,  *row will epand as positional args 
        else:
            user = None  # inclase row is empty 

        connection.close()
        return user  # return user object or None


    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))  # the only way to use parameters is to make it as a tuple (,) -> is used to maintain the tuple 
        row = result.fetchone()
        if row: 
            user = cls(*row) # makes a user object form class USER ,  *row will epand as positional args 
        else:
            user = None  # inclase row is empty 

        connection.close()
        return user  # return user object or None


class UserRegister(Resource):
    """ Registers users to the Database =>it will have resource , so we can add it to the api using Flask restful 
    
    Arguments:
        Resource {[type]} -- [description]
    """  


    parser = reqparse.RequestParser()
    
    #parser for username
    parser.add_argument('username',
        type=str, 
        required=True,
        help='this field is needed cant be skipped'
        )

    #parser for password 
    parser.add_argument('password',
        type=str,
        required=True,
        help='this field is needed cant be skipped'
        )


    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "user exist with that username"}, 400

        connection = sqlite3.connect('daba.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)" # NULL because to skip id
        cursor.execute(query, (data['username'], data['password']))

        connection.commit
        connection.close()
        
        return {"message": "User Created Successfully. "}, 201