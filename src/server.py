from flask import Flask
from flask_restful import Resource, Api
from db.main import buildTables, dropTables
from api.users import * 
from api.management import *
from api.communities import *
from api.chats import *
from api.auth import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Init, '/manage/init') #Management API for initializing the DB

api.add_resource(Version, '/manage/version') #Management API for checking DB version

api.add_resource(Test, '/manage/test') #API that gets called to load test data

api.add_resource(Users, '/users')

api.add_resource(User, '/users/<int:id>')

api.add_resource(Communities, '/communities')

api.add_resource(Chats, '/chats/<int:id>')

api.add_resource(DirectChats, '/users/<int:id_one>/direct/<int:id_two>')

api.add_resource(Auth, '/auth')


if __name__ == '__main__':
    dropTables()
    buildTables()
    app.run(debug=True)

