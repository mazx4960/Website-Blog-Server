from flask_restful import Api, Resource, reqparse

import sqlite3
import json

def get_db():
    db = sqlite3.connect('blog.sqlite3')
    db.row_factory = sqlite3.Row
    return db

class Users(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id")
        parser.add_argument("username")
        args = parser.parse_args()

        db = get_db()
        if args['user_id'] == None and args['username'] == None:
            user_data = db.execute('SELECT * FROM  Users').fetchall()
        else:
            user_data = db.execute('SELECT * FROM  Users WHERE user_id=? OR username=?',\
            (args['user_id'],args['username'])).fetchall()

        if user_data == []:
            return "User not found", 404
        else:
            users = []
            for user in user_data:
                temp = {
                    'user_id':user['user_id'],
                    'username':user['username'],
                    'password':user['password']
                }
                users.append(temp)
            return json.dumps(users), 200

    def post(self):
        db = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        args = parser.parse_args()

        # checking if user exists
        user_data = db.execute('SELECT * FROM  Users WHERE username=?',(args['username'],)).fetchall()
        if user_data != []:
            return "User already exists", 400

        db.execute('INSERT INTO Users (username,password) VALUES(?,?)', (args['username'],args['password']) )
        db.commit()
        return 201

    def put(self):
        pass

    def delete(self):
        pass
