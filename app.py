from flask import Flask
from flask_restful import Api, Resource, reqparse

from users import Users
from blogs import Blogs
from comments import Comments

app = Flask(__name__)
api = Api(app)

@route('/')
def index():
    return '<h1>The site is working!</h1>'

api.add_resource(Users, "/user")
api.add_resource(Blogs, "/blog")
api.add_resource(Comments, "/comment/<int:blog_id>")

app.run(debug=True)
