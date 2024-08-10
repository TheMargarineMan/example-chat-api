import unittest
import yaml
import os
from decimal import *
from datetime import *
from .test_chat import load_chat_data
from db.main import buildTables, dropTables
from db.messages import *
from db.users import addUser
from db.chats import addChat
from db.communities import addCommunity
from db.bans import banUser

def load_message_data():
    """Loads the test data for testing."""
    load_chat_data()
    data = {}
    yml_path = os.path.join(os.path.dirname(__file__), './test_data/test_message_data.yml')
    with open(yml_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    for key in data:
        addMessage(data[key]['message'], data[key]['user_id'], data[key]['chat_id'])

class TestMessage(unittest.TestCase):

    def setUp(self):
        """Resets tables for each test"""
        dropTables()
        buildTables()
          
    def test_rebuild_tables(self):
        """Rebuild the tables"""
        result = exec_get_all('SELECT * FROM messages')
        self.assertEqual([], result, "no rows in messages")

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        dropTables()
        buildTables()
        result = exec_get_all('SELECT * FROM messages')
        self.assertEqual([], result, "no rows in messages")

    def test_create_get_message(self):
        """Tests the creation and retrieval of a message."""
        load_chat_data()
        addMessage("Hello chat!", 1, 1)
        result = getChatHistory(1)
        expected = [(1, 'Hello chat!', False, result[0][3], 1, 1)] 
        self.assertEqual(expected, result)

    def test_get_extended_history(self):
        """Checks to see if able to get a proper message history."""
        load_message_data()
        result = getChatHistory(1)
        expected = [
            (5, 'Weirdo*', False, result[0][3], 3, 1),
            (4, 'Bruh wth are you talking about you wierdo', False, result[1][3], 1, 1),
            (3, 'The industrial revolution and its consequences part 1: ', False, result[2][3], 2, 1),
            (2, 'I like potatoes', False, result[3][3], 3, 1),
            (1, 'Hello friends!', False, result[4][3], 1, 1) 
        ]
        self.assertEqual(expected, result)
        
    def test_delete_message(self):
        """Checks to see if a message will get successfully deleted"""
        load_message_data()
        delMessage(3)
        result = getChatHistory(1)
        expected = [
            (5, 'Weirdo*', False, result[0][3], 3, 1),
            (4, 'Bruh wth are you talking about you wierdo', False, result[1][3], 1, 1),
            (2, 'I like potatoes', False, result[2][3], 3, 1),
            (1, 'Hello friends!', False, result[3][3], 1, 1) 
        ]
        self.assertEqual(expected, result)

    def test_edit_message(self):
        """Checks the ability to edit a message"""
        load_message_data()
        editMessage(3, "I did not quote the unibomber")
        result = getChatHistory(1)[2]
        expected = (3, "I did not quote the unibomber", True, result[3], 2, 1)
        self.assertEqual(expected, result)

class TestUnreadMessages(unittest.TestCase):

    def setUp(self):
        dropTables()
        buildTables()

    def test_generate_unread(self):
        """Creates a message and tests if the user has the unread message"""
        user_one = addUser("one", "password")
        user_two = addUser("two", "password")
        chat_id = addChat("Test")
        msg_id = addMessage("Test message", user_one, chat_id)
        generateUnreads(msg_id, [user_two])
        result = userGetUnreads(user_two)
        count = userGetUnreadCount(user_two)
        chat_result = userGetUnreadsChat(user_two, chat_id)
        chat_count = userGetUnreadChatCount(user_two, chat_id)
        expected = [(msg_id, "Test message", False, result[0][3], user_one, chat_id)]
        expected_count = 1
        self.assertEqual(count, expected_count)
        self.assertEqual(chat_count, expected_count)
        self.assertEqual(result, expected)
        self.assertEqual(chat_result, expected)

class TestMentions(unittest.TestCase):

    def setUp(self):
        dropTables()
        buildTables()
  
    def test_generate_mentions(self):
        """Creates a message and tests if it mentions a user"""
        user_one = addUser("one", "password")
        user_two = addUser("two", "password")
        chat_id = addChat("Test")
        msg_id = addMessage("Test message", user_one, chat_id)
        generateMentions(msg_id, [user_two])
        result = userGetMentions(user_two)
        expected = [(msg_id, "Test message", False, result[0][3], user_one, chat_id)]
        self.assertEqual(expected, result)


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        dropTables()
        buildTables()
        load_message_data()
  
    def test_search_chat(self):
        """Checks a search query for a chatroom"""
        result = queryChat(1, 'industrial')
        expected = [(3, 'The industrial revolution and its consequences part 1: ', False, result[0][3], 2, 1)]
        self.assertEqual(expected, result)

    def test_activity_summary(self):
        """Checks to see if gets a valid activity count"""
        getcontext().prec = 20
        result = activitySummary(1)
        expected = Decimal(len(getChatHistory(1)))/Decimal(30)
        self.assertEqual(expected, result)

    def test_mod_query(self):
        """Checks to see if is able to get a successful chat history of suspended users"""
        comm_id = addCommunity('test')
        chat_id = addChat('test_chat', comm_id)
        msg_one = addMessage('Ban me', 2, chat_id)
        msg_two = addMessage('*spreading hatred*', 2, chat_id)
        msg_three = addMessage('I will say mean things', 2, chat_id)
        msg_four = addMessage('I dont care that you broke your elbow', 2, chat_id)
        banUser(2, comm_id)
        result = modQuery(comm_id, datetime(2000, 1, 1), datetime.now())
        expected = [
            (msg_four, chat_id, 'Milkman', 'I dont care that you broke your elbow', False, result[0][5]),
            (msg_three, chat_id, 'Milkman', 'I will say mean things', False, result[1][5]),
            (msg_two, chat_id, 'Milkman', '*spreading hatred*', False, result[2][5]),
            (msg_one, chat_id, 'Milkman', 'Ban me', False, result[3][5])
        ]
        self.assertEqual(result, expected)
        