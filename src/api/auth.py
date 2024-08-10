from flask_restful import Resource, reqparse, request
import hashlib
from db.users import *

def auth_headers(req: request) -> bool:
    headers = req.headers
    user_id = headers.get('user-id')
    session_key = headers.get('session-key')
    if session_key is None or user_id is None:
        return False
    return sessionAuth(user_id, session_key)

class Auth(Resource):

    def post(self):
        body = request.get_json()
        if not ('username' in body.keys() and 'password' in body.keys()):
            return 'request needs username and password', 400
        user_id = getUserID(body['username'])
        if user_id is None:
            return 'user not found', 404
        hash = hashlib.sha512()
        hash.update(bytes(body['password'], 'utf-8'))
        pass_hash = hash.hexdigest()
        if passwordAuth(user_id, pass_hash):
            return {'user-id': str(user_id), 'session-key': genSessionKey(user_id)}, 200
        else:
            return 'authentication failed', 403
