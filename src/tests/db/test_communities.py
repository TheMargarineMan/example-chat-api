import unittest
from db.main import buildTables, dropTables
from db.communities import *
from db.chats import addChat
from db.users import addUser

class TestComm(unittest.TestCase):

	def setUp(self):
		"""Function that is run before every test"""
		dropTables()
		buildTables()

	def test_rebuild_table(self):
		"""Tests rebuilding the table"""
		result = exec_get_all('SELECT * FROM communities')
		self.assertEqual([], result)

	def test_rebuild_table_is_indepotent(self):
		"""Tests rebuilding twice"""
		dropTables()
		buildTables()
		result = exec_get_all('SELECT * FROM communities')
		self.assertEqual([], result)

	def test_add_get_community(self):
		"""Tests the creation and retrieval of a community"""
		id = addCommunity("Test")
		expected = [(1, "Test")]
		result = getCommunities()
		self.assertEqual(expected, result)

	def test_add_get_multiple(self):
		"""Tests the ability to have multiple communities"""
		id1 = addCommunity('PostgresSQL Support')
		id2 = addCommunity('psycopg2 Support')
		id3 = addCommunity('Using a Computer Support')
		expected = [(id1, 'PostgresSQL Support'), 
					(id2, 'psycopg2 Support'),
					(id3, 'Using a Computer Support')]
		result = getCommunities()
		self.assertEqual(expected, result)

class TestCommUser(unittest.TestCase):

	def setUp(self):
		"""Run before every test"""
		dropTables()
		buildTables()

	def test_rebuild_table(self):
		"""Tests rebuilding the table"""
		result = exec_get_all('SELECT * FROM comm_users')
		self.assertEqual([], result)

	def test_rebuild_table_is_indepotent(self):
		"""Tests rebuilding twice"""
		dropTables()
		buildTables()
		result = exec_get_all('SELECT * FROM comm_users')
		self.assertEqual([], result)

	def test_add_get_user(self):
		"""Tests adding and getting user in communities"""
		comm_id = addCommunity('test')
		user_id = addUser('user', 'randompassword')
		commAddUser(user_id, comm_id)
		result = commGetUsers(comm_id)
		expected = [(user_id, 'user')]
		self.assertEqual(result, expected)

