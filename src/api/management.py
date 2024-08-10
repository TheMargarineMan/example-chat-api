from flask_restful import Resource, reqparse, request  #NOTE: Import from flask_restful, not python

from db.main import *

class Init(Resource):
    def post(self):
        dropTables()
        buildTables()

class Version(Resource):
    def get(self):
        return (exec_get_one('SELECT VERSION()'))
 
class Test(Resource):
    def post(self):
        dropTables()
        buildTables()
        exec_sql_file('src/tests/db/test_data/test_data.sql')
