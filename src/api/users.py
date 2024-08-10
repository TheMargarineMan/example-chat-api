from flask import jsonify
from flask_restful import Resource, reqparse, request
from psycopg2.errors import UniqueViolation
import hashlib
from db.users import *
from api.auth import auth_headers

def generateUserDicts(users: list) -> list:
	"""Takes a list of raw user data and generates a list of dicts"""
	return [{
		'id': n[0],
		'username': n[1]} 
		for n in users]

class Users(Resource):

	def get(self):
		if not auth_headers(request): return 'auth failed', 403
		return generateUserDicts(getUsers()) 

	def post(self):
		body = request.get_json()
		if not ('username' in body.keys() and 'password' in body.keys()):
			return 'request needs username and password', 400
		try:
			hash = hashlib.sha512()
			pass_bytes = bytes(body['password'], 'utf-8')
			hash.update(pass_bytes)
			digest = hash.hexdigest()
			return addUser(body['username'], digest), 201
		except UniqueViolation:
			return 'user with username exists', 409 

class User(Resource):

	def get(self, id: int):
		if not auth_headers(request): return 'auth failed', 403
		userInfo = getUser(id)
		if userInfo is None:
			return 'user not found', 404
		return {
			'id': userInfo[0],
			'username': userInfo[1],
			'active': userInfo[2]
		}
		
	def put(self, id: int):		
		if not auth_headers(request): return 'auth failed', 403
		body = request.get_json()
		for key in body.keys():
			if key == 'username':
				try:
					if not nameChangeCheck(id):
						return 'user changed username in last 6 months', 403
					setUsername(id, body[key])
					nameChangeTimeout(id)
				except UniqueViolation:
					return 'user with username exists', 409 
			elif key == 'password':
				setPassword(id, body[key])
		return 200
				
	def delete(self, id: int):
		if not auth_headers(request): return 'auth failed', 403
		if getUser(id) is None:
			return 'user not found', 404
		deactivateUser(id)
		return 200
