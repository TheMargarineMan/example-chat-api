import unittest
import yaml
import os
from .test_user import load_user_data
from db.chats import *
from db.main import dropTables, buildTables


def load_chat_data():
    """Loads the test data for testing."""
    load_user_data()  
    data = {}
    yml_path = os.path.join(os.path.dirname(__file__), './test_data/test_chat_data.yml')
    with open(yml_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    for key in data:
        addChat(data[key]['chat_name'])

class TestChat(unittest.TestCase):

    def setUp(self):
        """Resets tables for each test"""
        dropTables()
        buildTables()
            
    def test_rebuild_tables(self):
        """Rebuild the tables"""
        result = exec_get_all('SELECT * FROM chats')
        self.assertEqual([], result, "no rows in chats")

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        dropTables()
        buildTables()
        result = exec_get_all('SELECT * FROM chats')
        self.assertEqual([], result, "no rows in chats")

    def test_create_get_chatroom(self):
        """Test creation tool for chatrooms"""
        chat_id = addChat("General")
        expected = (chat_id, "General", None)
        result = getChat(chat_id)
        self.assertEqual(expected, result)

    def test_get_chatrooms(self):
        """Test the retrieval of multiple chatrooms"""
        load_chat_data()
        result = getChats()
        expected = [(1, "General", None), (2, "Memes and Stuff", None)]
        self.assertEqual(expected, result)

def load_user_chat_data():
    """Loads the test data for testing"""
    load_chat_data()
    data = {}
    yml_path = os.path.join(os.path.dirname(__file__), './test_data/test_user_chat_data.yml')    
    with open(yml_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    for key in data:
        chatAddUser(data[key]['user_id'], data[key]['chat_id'])
    
class TestUserChat(unittest.TestCase):

    def setUp(self):
        """Resets tables for each test"""
        dropTables()
        buildTables()

    def test_add_user_to_chat(self):
        """Tests adding and retrieving a user to a chatroom"""
        load_chat_data()
        chatAddUser(1, 1)
        result = chatGetUsers(1)
        expected = [(1, 'Davie504')]
        self.assertEqual(expected, result)

    def test_get_users_in_chat(self):
        """Tests the getting of all users related to a chatroom"""
        load_user_chat_data()
        result1 = chatGetUsers(1)
        result2 = chatGetUsers(2)
        expected1 = [(1, 'Davie504'), (2, 'Milkman'), (3, 'swapnila')]
        expected2 = [(1, 'Davie504'), (3, 'swapnila')]
        self.assertEqual(expected1, result1)
        self.assertEqual(expected2, result2)

    def test_get_user_in_chats(self):
        """Tests the getting of all chats a user is in"""
        load_user_chat_data()
        result1 = userGetChats(1)
        result2 = userGetChats(2)
        result3 = userGetChats(3)
        expected1 = [(1, 'General'), (2, 'Memes and Stuff')]
        expected2 = [(1, 'General')]
        self.assertEqual(expected1, result1)
        self.assertEqual(expected2, result2)
        self.assertEqual(expected1, result3)

    def test_remove_user_from_chat(self):
        """Tests the removal of a user from a chatroom"""
        load_user_chat_data()
        chatDelUser(1, 2)
        result = chatGetUsers(2)
        expected = [(3, 'swapnila')]
        self.assertEqual(expected, result)
class TestDirectChat(unittest.TestCase):

    def setUp(self):
        dropTables()
        buildTables()

    def test_add_get_direct_chat(self):
        """Tests the addition of a chat as a direct chat"""
        load_user_data()
        chat_id = addChat("DM(Test)")
        addDirectChat(1, 2, chat_id)
        result1 = getDirectChat(1, 2)
        result2 = getDirectChat(2, 1)
        self.assertEqual(chat_id, result1)
        self.assertEqual(result1, result2)

    def test_add_get_multiple_chats(self):
        """Tests the creation of multiple direct chats"""
        load_user_data()
        chat_one = addChat("DM(1,2)")
        chat_two = addChat("DM(2,3)")
        chat_three = addChat("DM(1,3)")
        addDirectChat(1, 2, chat_one)
        addDirectChat(2, 3, chat_two)
        addDirectChat(1, 3, chat_three)
        result1 = getDirectChats(1)
        result2 = getDirectChats(2)
        result3 = getDirectChats(3)
        expected1 = [chat_one, chat_three]
        expected2 = [chat_one, chat_two]
        expected3 = [chat_two, chat_three]
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
