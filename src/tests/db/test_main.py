import unittest
import csv
import os
from db.main import *
from db.chats import *

def load_test_data() -> list:
    """Loads whos_on_first.csv for testing"""
    data = []
    data_path = os.path.join(os.path.dirname(__file__), './test_data/whos_on_first.csv')
    with open(data_path, 'r') as file:
        reader = csv.reader(file)
        reader.__next__()
        for row in reader:
            name = row[0]
            message = ", ".join(row[1:]).strip()
            data.append((name, message))
    return data

class TestMain(unittest.TestCase):
    
    def setUp(self):
        dropTables()
        buildTables()
    
    def test_storing_chat_history(self):
        data = load_test_data()
        abbott = addUser('Abbott', 'password123')
        costello = addUser('Costello', 'pass123')
        chat_id = addChat('test')
        expected = []
        for entry in data:
            if entry[0] == 'Abbott':
                sendMessage(abbott, entry[1], chat_id)
                expected.append((abbott, entry[1]))
            elif entry[0] == 'Costello':
                sendMessage(costello, entry[1], chat_id)
                expected.append((costello, entry[1]))
        expected = expected[len(expected)-1::-1]
        history = getChatHistory(chat_id, {'limit': None})
        result = []
        for entry in history:
            result.append((entry[4], entry[1]))
        self.assertEqual(expected, result)