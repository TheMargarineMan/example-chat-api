import unittest 
from tests.test_utils import *
from tests.api.test_auth import getHeaders

class TestChats(unittest.TestCase):

    data = [
    {
        "id": 9,
        "message": "The man who about to steal ur girl",
        "edited": False,
        "timestamp": "2012-07-25 10:08:11",
        "user_id": 1
    },
    {
        "id": 8,
        "message": "Now who is this bozo",
        "edited": False,
        "timestamp": "2012-07-25 10:08:04",
        "user_id": 2
    },
    {
        "id": 7,
        "message": "Nah fam cant have that",
        "edited": False,
        "timestamp": "2012-07-24 04:21:01",
        "user_id": 9
    },
    {
        "id": 6,
        "message": "Sup I run this block now",
        "edited": False,
        "timestamp": "2012-07-24 04:20:40",
        "user_id": 1
    },
    {
        "id": 5,
        "message": "Honey, Im home from my vacation! Wait wtf.",
        "edited": False,
        "timestamp": "2012-07-24 04:20:22",
        "user_id": 9
    },
    {
        "id": 4,
        "message": "KNEEL BEFORE MORGOTT, THE OMEN KING",
        "edited": False,
        "timestamp": "2012-06-24 12:43:20",
        "user_id": 10
    },
    {
        "id": 3,
        "message": "Your ego is as fragile as your title of King",
        "edited": False,
        "timestamp": "2012-06-24 12:43:10",
        "user_id": 4
    },
    {
        "id": 2,
        "message": "My brother in Marika you wear rags as a monarch. The Golden Order fell off.",
        "edited": False,
        "timestamp": "2012-06-24 12:43:05",
        "user_id": 1
    },
    {
        "id": 1,
        "message": "Fools emboldened by the flame of ambition.",
        "edited": False,
        "timestamp": "2012-06-24 12:42:57",
        "user_id": 10
    }
    ]

    headers = None

    def setUp(self):
        post_rest_call(self, 'http://localhost:5000/manage/test')
        self.headers = getHeaders(self, 'xX_EldenLord_Xx', 'thefallenleaves')        

    def testGetAllMessages(self):
        # curl -X GET 'http://localhost:5000/chats/3'
        result = get_rest_call(self, 'http://localhost:5000/chats/3', get_header=self.headers)
        expected = self.data
        self.assertEqual(expected, result)

    def testGetMessagesFromUser(self):
        result = get_rest_call(self, 'http://localhost:5000/chats/3?user=1', get_header=self.headers)
        expected = [self.data[0], self.data[3], self.data[7]]
        self.assertEqual(expected, result)

    def testGetMessagesBefore(self):
        result = get_rest_call(self, 'http://localhost:5000/chats/3?before=2012-6-25', get_header=self.headers)
        expected = self.data[5:9]
        self.assertEqual(expected, result)

    def testGetMessagesAfter(self):
        result = get_rest_call(self, 'http://localhost:5000/chats/3?after=2012-6-25', get_header=self.headers)
        expected = self.data[0:5]
        self.assertEqual(expected, result)

    def testGetMessagesRange(self):
        result = get_rest_call(self, 'http://localhost:5000/chats/3?before=2012-7-25&after=2012-6-25', get_header=self.headers)
        expected = self.data[2:5]
        self.assertEqual(expected, result)

    def testGetMessagesContains(self):
        result = get_rest_call(self, 'http://localhost:5000/chats/3?contains=is', get_header=self.headers)
        expected = [self.data[1], self.data[3], self.data[6]]
        self.assertEqual(expected, result)

    def testGetMessagesContainsFromUser(self):
        result = get_rest_call(self, 'http://localhost:5000/chats/3?user=1&contains=is', get_header=self.headers)
        expected = [self.data[3]]
        self.assertEqual(expected, result)

class TestDirectChats(unittest.TestCase):

    data = [    
    {
        "id": 12,
        "message": "*disappears*",
        "edited": False,
        "timestamp": "2010-07-25 10:10:14",
        "user_id": 9
    },
    {
        "id": 11,
        "message": "Wait, no father please",
        "edited": False,
        "timestamp": "2010-07-25 10:10:12",
        "user_id": 10
    },
    {
        "id": 10,
        "message": "Ima dip out son",
        "edited": False,
        "timestamp": "2010-07-25 10:10:10",
        "user_id": 9
    },
    ]

    headers = None

    def setUp(self):
        post_rest_call(self, 'http://localhost:5000/manage/test')
        self.headers = getHeaders(self, 'xX_EldenLord_Xx', 'thefallenleaves')

    def testGetAllDirectMessages(self):
        result = get_rest_call(self, 'http://localhost:5000/users/10/direct/9', get_header=self.headers)
        expected = self.data
        self.assertEqual(expected, result)

        result = get_rest_call(self, 'http://localhost:5000/users/9/direct/10', get_header=self.headers)
        self.assertEqual(expected, result)
