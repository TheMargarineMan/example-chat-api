import unittest
from tests.test_utils import *

class TestCommunities(unittest.TestCase):

    def setUp(self):
        post_rest_call(self, 'http://localhost:5000/manage/test')

    def testGetAllCommunities(self):
        # curl -X GET 'http://localhost:5000/communities'
        result = get_rest_call(self, 'http://localhost:5000/communities')
        expected = [
            {'id': 1, 'name': 'Raya Lucaria', 'chats': [
                {'id': 1, 'name': 'Grand Study Hall'},
                {'id': 2, 'name': 'Rannis Rise'}
            ]},
            
            {'id': 2, 'name': 'Leyendell', 'chats': [
                {'id': 3, 'name': 'The Foot of the Erdtree'},
                {'id': 4, 'name': 'Erdtree Sanctuary'}
            ]},
            
            {'id': 3, 'name': 'Redmane Castle', 'chats': [
                {'id': 5, 'name': 'Radahns Battlefield'},
                {'id': 6, 'name': 'The Divine Tower of Caelid'}
            ]}
        ]
        self.assertEqual(expected, result)