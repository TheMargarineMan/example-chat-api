import unittest
import yaml
import os
from psycopg.errors import UniqueViolation
from db.users import *
from db.main import dropTables, buildTables

def load_user_data():
	"""Loads test data"""
	data = {}
	yml_path = os.path.join(os.path.dirname(__file__), './test_data/test_user_data.yml')		
	with open(yml_path, 'r') as file:
		data = yaml.load(file, Loader=yaml.FullLoader)
	for key in data:
		addUser(data[key]['username'], data[key]['password'])
		
class TestUser(unittest.TestCase):

	def setUp(self):
		"""Rebuilds table for each test"""
		dropTables()
		buildTables()

	def test_rebuild_tables(self):
		"""Rebuilds table once"""
		result = exec_get_all('SELECT * FROM users')
		self.assertEqual([], result, "no rows in users")

	def test_rebuild_tables_is_idempotent(self):
		"""Revuilds table twice"""
		dropTables()
		buildTables()
		result = exec_get_all('SELECT * FROM users')
		self.assertEqual([], result, "no rows in users")

	def test_add_retrieve_user(self):
		"""Tests creation and retrieval of users"""
		user_id = addUser('Davie504', 'password123')
		result = getUser(user_id)
		expected = (1, 'Davie504', True)
		self.assertEqual(result, expected)

	def test_add_user_conflict(self):
		"""Tests adding user if there is already a user with the name listed"""
		load_user_data()
		try:
			addUser('Davie504', '321drowssap')
			self.assertTrue(False)
		except UniqueViolation:
			self.assertTrue(True)
	
	def test_set_username(self):
		"""Tests setting username on an existing user"""
		load_user_data()		
		setUsername(1, 'bomberman')
		result = getUser(1)
		expected = (1, 'bomberman', True)
		self.assertEqual(result, expected)

	def test_set_username_conflict(self):
		"""Tests setting name on an existing user when the username is taken"""
		load_user_data()
		try:
			setUsername(1, 'Milkman')
			self.assertTrue(False)
		except UniqueViolation:
			self.assertTrue(True)