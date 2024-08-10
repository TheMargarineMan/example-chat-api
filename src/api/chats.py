from flask import Flask
from flask_restful import Resource, reqparse, request
from datetime import *
from api.auth import auth_headers
from db.users import getUser
from db.chats import *
from db.messages import *

def generateChatDicts(chats: list) -> list:
	"""Takes a list of raw chat data and generates a list of dicts"""
	return [{
		'id': n[0],
		'name': n[1]
	} 
	for n in chats]

def generateMessageDicts(messages: list) -> list:
	"""Takes a list of raw messages and generates a list of dicts"""
	return [{
		'id': n[0],
		'message': n[1],
		'edited': n[2],
		'timestamp': n[3].strftime("%Y-%m-%d %H:%M:%S"),
		'user_id': n[4]
	}
	for n in messages]	

class Chats(Resource):

	def get(self, id: int):
		if not auth_headers(request): return 'auth failed', 403
		args = request.args.to_dict()
		if getChat(id) is None:
			return 404
		return generateMessageDicts(getChatHistory(id, args)) 

class DirectChats(Resource):

	def get(self, id_one: int, id_two: int):
		if not auth_headers(request): return 'auth failed', 403
		args = request.args.to_dict()
		chatID = getDirectChat(id_one, id_two)
		if (getUser(id_one) is None) or (getUser(id_two) is None):
			return 'One or more users do not exist', 400
		elif chatID is None:
			return 404
		return generateMessageDicts(getChatHistory(chatID, args))
		
