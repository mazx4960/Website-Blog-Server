from flask_restful import Api, Resource, reqparse

import sqlite3
import json

def get_db():
    db = sqlite3.connect('blog.sqlite3')
    db.row_factory = sqlite3.Row
    return db

class Blogs(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("blog_id")
        parser.add_argument("blogger_id")
        args = parser.parse_args()

        db = get_db()
        if args['blog_id'] == None and args['blogger_id'] == None:
            blog_data = db.execute('SELECT * FROM  Blogs').fetchall()
        else:
            blog_data = db.execute('SELECT * FROM  Blogs WHERE blog_id=? OR blogger_id=?',\
            (args['blog_id'],args['blogger_id'])).fetchall()

        if blog_data == []:
            return json.dumps([]), 200

        blogs = []
        for blog in blog_data:
            temp = {
                'blog_id': blog['blog_id'],
                'blogger_id':blog['blogger_id'],
                'post':blog['post']
            }
            blogs.append(temp)

        return json.dumps(blogs), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("blogger_id", required=True)
        parser.add_argument("post", required=True)
        args = parser.parse_args()

        db = get_db()
        user_data = db.execute('SELECT * FROM  Users WHERE user_id=?',(args['blogger_id'],))
        if user_data == []:
            return "User is not registered yet", 404

        db.execute('INSERT INTO Blogs (blogger_id,post) VALUES (?, ?)' , (args['blogger_id'], args['post']))
        db.commit()
        return 201

    def put(self):
        pass

    def delete(self):
        pass
