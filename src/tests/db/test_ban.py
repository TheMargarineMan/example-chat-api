import unittest

from db.main import dropTables, buildTables
from db.users import addUser
from db.communities import addCommunity, commAddUser, commGetUsers
from db.bans import *

class TestBan(unittest.TestCase):

    def setUp(self):
        dropTables()
        buildTables()
        
    def test_ban_check_false(self):
        user_id = addUser('Gamerman', 'gamerpassword')
        comm_id = addCommunity('Test Comm')
        commAddUser(user_id, comm_id)
        user_list = commGetUsers(comm_id)
        self.assertFalse(banCheck(user_id, comm_id))
        self.assertEqual([(user_id, 'Gamerman')], user_list)

    def test_ban_user(self):
        user_id = addUser('Gamerman', 'gamerpassword')
        comm_id = addCommunity('Test Comm')
        commAddUser(user_id, comm_id)

        banUser(user_id, comm_id)

        user_list = commGetUsers(comm_id)
        self.assertTrue(banCheck(user_id, comm_id))
        self.assertEqual([], user_list)

    def test_pardon_user(self):
        user_id = addUser('Gamerman', 'gamerpassword')
        comm_id = addCommunity('Test Comm')
        commAddUser(user_id, comm_id)

        banUser(user_id, comm_id)
        pardonUser(user_id, comm_id)
        
        user_list = commGetUsers(comm_id)
        self.assertFalse(banCheck(user_id, comm_id))
        self.assertEqual([], user_list)

    def test_comm_get_bans(self):
        user_id = addUser('Gamerman', 'gamerpassword')
        comm_id = addCommunity('Test Comm')
        commAddUser(user_id, comm_id)

        bans = commGetBans(comm_id)
        self.assertEqual(bans, [])

        banUser(user_id, comm_id)

        bans = commGetBans(comm_id)

        self.assertEqual(bans, [(user_id, 'Gamerman')])

    def test_user_get_bans(self):        
        user_id = addUser('Gamerman', 'gamerpassword')
        comm_id = addCommunity('Test Comm')
        commAddUser(user_id, comm_id)

        bans = userGetBans(user_id)
        self.assertEqual(bans, [])

        banUser(user_id, comm_id)

        bans = userGetBans(user_id)

        self.assertEqual(bans, [(comm_id, 'Test Comm')])

