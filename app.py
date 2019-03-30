from flask import Flask
from flask_restful import Api, Resource, reqparse

import sqlite3
import json

app = Flask(__name__)
api = Api(app)

def get_db():
    db = sqlite3.connect('blog.sqlite3')
    db.row_factory = sqlite3.Row
    return db


########################### Users class ###########################


class Users(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id")
        parser.add_argument("username")
        parser.add_argument("email")
        args = parser.parse_args()

        db = get_db()
        if args['user_id'] == None and args['username'] == None:
            user_data = db.execute('SELECT * FROM  Users').fetchall()
        else:
            user_data = db.execute('SELECT * FROM  Users WHERE user_id=? OR username=? OR email=?',\
            (args['user_id'],args['username'],args['email'])).fetchall()

        if user_data == []:
            return "User not found", 404
        else:
            users = []
            for user in user_data:
                temp = {
                    'user_id' : user['user_id'],
                    'username': user['username'],
                    'password': user['password'],
                    'email'   : user['email'],
                    'admin'   : user['admin']
                }
                users.append(temp)
            return json.dumps(users), 200

    def post(self):
        db = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("email", required=True)
        parser.add_argument("admin", required=True)
        args = parser.parse_args()

        # checking if user exists
        user_data = db.execute('SELECT * FROM  Users WHERE username=?',(args['username'],)).fetchall()
        if user_data != []:
            return "User already exists", 400

        db.execute('INSERT INTO Users (username,password,email,admin) \
        VALUES(?,?,?,?)', (args['username'],args['password'],args['email'],args['admin']) )

        db.commit()
        return 201

    def put(self):
        db = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True)
        parser.add_argument("password")
        parser.add_argument("email")
        parser.add_argument("admin")
        args = parser.parse_args()

        # checking if user exists
        user_data = db.execute('SELECT * FROM  Users WHERE user_id=?',(args['user_id'],)).fetchall()
        if user_data == []:
            return "User does not exists", 400

        if args['password'] != None:
            db.execute('UPDATE Users SET password=? WHERE user_id=?', (args['password'],args['user_id']))

        if args['email'] != None:
            db.execute('UPDATE Users SET email=? WHERE user_id=?', (args['email'],args['user_id']))

        if args['admin'] != None:
            db.execute('UPDATE Users SET admin=? WHERE user_id=?', (args['admin'],args['user_id']))

        db.commit()
        return 200

    def delete(self):
        db = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True)
        args = parser.parse_args()

        # checking if user exists
        user_data = db.execute('SELECT * FROM  Users WHERE user_id=?',(args['user_id'],)).fetchall()
        if user_data == []:
            return "User does not exists", 400

        db.execute('DELETE FROM Users WHERE user_id=?', (args['user_id']))
        db.commit()
        return 200


########################### Friendships class ###########################


class Friendships(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True)
        args = parser.parse_args()

        db = get_db()
        friendships_data = db.execute('SELECT * FROM  Friendships WHERE user_id1=? OR user_id2=?', (args['user_id'],args['user_id'])).fetchall()

        if friendships_data == []:
            return json.dumps({}), 200
        else:
            friends = {}
            for friend in friendships_data:
                # you are the sender and status is pending
                if str(args['user_id']) == str(friend['user_id1']) and friend['status'] == 'pending':
                    friends[friend['user_id2']] = 'sent'
                # the other party is the sender
                elif str(args['user_id']) == str(friend['user_id2']):
                    friends[friend['user_id1']] = friend['status']
                # you are the sender
                else:
                    friends[friend['user_id2']] = friend['status']

            return json.dumps(friends), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True)
        parser.add_argument("friend_id", required=True)
        parser.add_argument("timestamp", required=True)
        parser.add_argument("status", required=True)
        args = parser.parse_args()

        db = get_db()
        # checking if friendship exists
        friendships_data = db.execute('SELECT * FROM  Friendships \
        WHERE (user_id1=? AND user_id2=?) OR (user_id1=? AND user_id2=?)',\
        (args['user_id'],args['friend_id'],args['friend_id'],args['user_id'])).fetchall()

        if friendships_data != []:
            return "Friendship already exists", 400

        db.execute('INSERT INTO Friendships (user_id1,user_id2,timestamp,status) \
        VALUES(?,?,?,?)', (args['user_id'],args['friend_id'],args['timestamp'],args['status']) )

        db.commit()
        return 201

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True)
        parser.add_argument("friend_id", required=True)
        parser.add_argument("status", required=True)
        args = parser.parse_args()

        db = get_db()
        # checking if friendship exists
        friendships_data = db.execute('SELECT * FROM  Friendships \
        WHERE (user_id1=? AND user_id2=?) OR (user_id1=? AND user_id2=?)',\
        (args['user_id'],args['friend_id'],args['friend_id'],args['user_id'])).fetchall()

        if friendships_data == []:
            return "Friendship not found", 404

        db.execute('UPDATE Friendships SET status=? WHERE (user_id1=? AND user_id2=?) OR (user_id1=? AND user_id2=?)',\
        (args['status'],args['user_id'],args['friend_id'],args['friend_id'],args['user_id']))

        db.commit()
        return 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", required=True)
        parser.add_argument("friend_id", required=True)
        args = parser.parse_args()

        db = get_db()
        # checking if friendship exists
        friendships_data = db.execute('SELECT * FROM  Friendships \
        WHERE (user_id1=? AND user_id2=?) OR (user_id1=? AND user_id2=?)',\
        (args['user_id'],args['friend_id'],args['friend_id'],args['user_id'])).fetchall()

        if friendships_data == []:
            return "Friendship not found", 404

        db.execute('DELETE FROM Friendships WHERE (user_id1=? AND user_id2=?) OR (user_id1=? AND user_id2=?)',\
        (args['user_id'],args['friend_id'],args['friend_id'],args['user_id']))
        db.commit()
        return 200


########################### Blogs Class ###########################


class Blogs(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("blog_id")
        parser.add_argument("blogger_id")
        args = parser.parse_args()

        db = get_db()
        if args['blog_id'] == None and args['blogger_id'] == None:
            blog_data = db.execute('SELECT * FROM Blogs').fetchall()
        else:
            blog_data = db.execute('SELECT * FROM Blogs WHERE blog_id=? OR blogger_id=?',\
            (args['blog_id'],args['blogger_id'])).fetchall()

        if blog_data == []:
            return json.dumps([]), 200

        blogs = []
        for blog in blog_data:
            temp = {
                'blog_id'   :blog['blog_id'],
                'blogger_id':blog['blogger_id'],
                'post'      :blog['post'],
                'timestamp' :blog['timestamp']
            }
            blogs.append(temp)

        return json.dumps(blogs), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("blogger_id", required=True)
        parser.add_argument("post", required=True)
        parser.add_argument("timestamp", required=True)
        args = parser.parse_args()

        db = get_db()
        user_data = db.execute('SELECT * FROM  Users WHERE user_id=?',(args['blogger_id'],))
        if user_data == []:
            return "User is not registered yet", 404

        db.execute('INSERT INTO Blogs (blogger_id,post,timestamp) \
        VALUES (?, ?, ?)' , (args['blogger_id'], args['post'], args['timestamp']))
        db.commit()
        return 201

    def put(self):
        pass

    def delete(self):
        pass


########################### Comments Class ###########################


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


########################### Routes ###########################


@app.route('/')
def index():
    return '<h1>The site is working!</h1>'

api.add_resource(Users, "/user")
api.add_resource(Friendships, "/friendship")
api.add_resource(Blogs, "/blog")
api.add_resource(Comments, "/comment/<int:blog_id>")


########################### End of file ###########################
