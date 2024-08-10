from flask_restful import Resource, reqparse, request

from db.communities import *
from db.chats import *
from api.chats import generateChatDicts

def generateCommDicts(comms: list) -> list:
	"""Takes a list of raw comm data and generates a list of dicts"""
	return [{
		'id': n[0],
		'name': n[1],
        'chats': generateChatDicts(commGetChats(n[0]))}
		for n in comms]
		

class Communities(Resource):
    def get(self):
        return generateCommDicts(getCommunities())