import unittest
import json
from tests.test_utils import *
from tests.api.test_auth import getHeaders

class TestUsers(unittest.TestCase):

	headers = None
	
	def setUp(self):
		post_rest_call(self, 'http://localhost:5000/manage/test')
		self.headers = getHeaders(self, 'xX_EldenLord_Xx', 'thefallenleaves')

	def testGetAllUsers(self):
		# curl -X GET 'http://localhost:5000/users'
		print(self.headers)
		print(self.headers)
		
		result = get_rest_call(self, 'http://localhost:5000/users', get_header=self.headers)
		expected = [
			{ 'id': 1, 'username': 'xX_EldenLord_Xx'},
			{ 'id': 2, 'username': 'Radagon'},
			{ 'id': 3, 'username': 'Mal3n1a'},
			{ 'id': 4, 'username': 'Melina'},
			{ 'id': 5, 'username': 'Ranni'},
			{ 'id': 6, 'username': 'Brother Corhyn'},
			{ 'id': 7, 'username': 'Starscourge'},
			{ 'id': 8, 'username': 'GildedGraft'},
			{ 'id': 9, 'username': 'Godfrey'},
			{ 'id': 10, 'username': 'Morgott'}
		]
		self.assertEqual(10, len(result))
		self.assertEqual(expected, result)

	def testGetUser(self):
		result = get_rest_call(self, 'http://localhost:5000/users/2', get_header=self.headers)
		expected = {
			'id': 2,
			'username': 'Radagon',
			'active': True
		}
		self.assertEqual(expected, result)

	def testPostUser(self):
		# curl -X POST -H "Content-Type: application/json" -d '{"username": "Marika", "password": "shattering"}' 'http://localhost:5000/users'
		newUser = {
			'username': 'Marika',
			'password': 'shattering'
		}
		result = post_rest_call(self, 'http://localhost:5000/users', params=json.dumps(newUser), post_header=self.headers, expected_code=201)
		expected = 11 # UserID returned
		self.assertEqual(expected, result)
		result = get_rest_call(self, 'http://localhost:5000/users', get_header=self.headers)
		expected = [
			{ 'id': 1, 'username': 'xX_EldenLord_Xx'},
			{ 'id': 2, 'username': 'Radagon'},
			{ 'id': 3, 'username': 'Mal3n1a'},
			{ 'id': 4, 'username': 'Melina'},
			{ 'id': 5, 'username': 'Ranni'},
			{ 'id': 6, 'username': 'Brother Corhyn'},
			{ 'id': 7, 'username': 'Starscourge'},
			{ 'id': 8, 'username': 'GildedGraft'},
			{ 'id': 9, 'username': 'Godfrey'},
			{ 'id': 10, 'username': 'Morgott'},
			{ 'id': 11, 'username': 'Marika'}
		]
		self.assertEqual(expected, result)

	def testPutUser(self):
		newUserData = {
			'username': 'Marika',
			'password': 'shattering'
		}
		result = put_rest_call(self, 'http://localhost:5000/users/2', params=json.dumps(newUserData), put_header=self.headers)
		expected = 200
		self.assertEqual(expected, result)		
		
		result = get_rest_call(self, 'http://localhost:5000/users', get_header=self.headers)
		expected = [
			{ 'id': 1, 'username': 'xX_EldenLord_Xx'},
			{ 'id': 2, 'username': 'Marika'},
			{ 'id': 3, 'username': 'Mal3n1a'},
			{ 'id': 4, 'username': 'Melina'},
			{ 'id': 5, 'username': 'Ranni'},
			{ 'id': 6, 'username': 'Brother Corhyn'},
			{ 'id': 7, 'username': 'Starscourge'},
			{ 'id': 8, 'username': 'GildedGraft'},
			{ 'id': 9, 'username': 'Godfrey'},
			{ 'id': 10, 'username': 'Morgott'},
		]
		self.assertEqual(expected, result)

		newUserData = {
			'username': 'Radagon'
		}
		result = put_rest_call(self, 'http://localhost:5000/users/2', params=json.dumps(newUserData), put_header=self.headers, expected_code=403)
		expected = 'user changed username in last 6 months'
		self.assertEqual(expected, result)

	def testDelUser(self):
		result = delete_rest_call(self, 'http://localhost:5000/users/2', delete_header=self.headers)
		expected = 200
		self.assertEqual(expected, result)

		result = get_rest_call(self, 'http://localhost:5000/users/2', get_header=self.headers)
		expected = {
			'id': 2,
			'username': 'Radagon',
			'active': False
		}
		self.assertEqual(expected, result)

		result = get_rest_call(self, 'http://localhost:5000/users', get_header=self.headers)
		expected = [
			{ 'id': 1, 'username': 'xX_EldenLord_Xx'},
			{ 'id': 3, 'username': 'Mal3n1a'},
			{ 'id': 4, 'username': 'Melina'},
			{ 'id': 5, 'username': 'Ranni'},
			{ 'id': 6, 'username': 'Brother Corhyn'},
			{ 'id': 7, 'username': 'Starscourge'},
			{ 'id': 8, 'username': 'GildedGraft'},
			{ 'id': 9, 'username': 'Godfrey'},
			{ 'id': 10, 'username': 'Morgott'},
		]
		self.assertEqual(expected, result)
