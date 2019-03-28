from flask_restful import Api, Resource, reqparse

import sqlite3
import json

def get_db():
    db = sqlite3.connect('blog.sqlite3')
    db.row_factory = sqlite3.Row
    return db

class Comments(Resource):
    def get(self, blog_id):
        db = get_db()
        comment_data = db.execute('SELECT * FROM Comments WHERE blog_id=?', (blog_id,)).fetchall()
        if comment_data == []:
            return json.dumps([]), 200

        comments = []
        for comment in comment_data:
            temp = {
                'comment_id': comment['comment_id'],
                'user_id': comment['user_id'],
                'comment': comment['comment'],
                'blog_id': comment['blog_id']
            }
            comments.append(temp)

        return json.dumps(comments), 200

    def post(self, blog_id):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id")
        parser.add_argument("comment")
        args = parser.parse_args()

        db = get_db()
        user_data = db.execute('SELECT * FROM  Users WHERE user_id=?',(args['user_id'],))
        if user_data == []:
            return "User is not registered yet", 404

        db.execute('INSERT INTO Comments (user_id,comment,blog_id) \
        VALUES(?,?,?)', (args['user_id'],args['comment'],blog_id))
        db.commit()
        return 201

    def put(self, blog_id):
        pass

    def delete(self, blog_id):
        pass
