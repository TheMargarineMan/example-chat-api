from db.chats import *
from db.messages import *
from db.users import *
from db.communities import *
from db.bans import *
from db.__init__ import exec_sql_file
from psycopg.errors import UniqueViolation
import re

def buildTables() -> None:
    """Builds all tables within the schema"""
    exec_sql_file('src/db/schema.sql')

def dropTables() -> None:
    exec_sql_file('src/db/drop_schema.sql')

def getUsersInChat(chat_id: int) -> list:
    """
    Gets all users in a chatroom.
    If the chat has an owner (comm_id), it will default to the owner's user_list
    Else it will use its own.
    """
    comm_id = chatGetComm(chat_id)
    if comm_id is None:
        return chatGetUsers(chat_id)
    else:
        return commGetUsers(comm_id)     

def parseMentions(message: str) -> list:
    """Parses a message data for mentioned users"""
    mentions = re.findall(r'\@\w+', message)
    result = []
    for mention in mentions:
        user_id = getUserID(mention[1:])
        if (user_id is not None):
            result.append(user_id)
    return result

def sendMessage(user_id: int, message: str, chat_id: int) -> None:
    """Checks if banned, then sends a message to chatroom"""
    mentions = parseMentions(message)
    chat_users = getUsersInChat(chat_id)
    msg_id = addMessage(message, user_id, chat_id)
    generateUnreads(msg_id, chat_users)
    generateMentions(msg_id, mentions)

def directMessage(sender: int, recipient: int, auth_token: str, message: str) -> None:
    """Sends a direct message to another user. Creates a new room if it doesnt exist"""
    chat_id = getDirectChat(sender, recipient)
    if chat_id is None:
        chat_id = addChat(f'DM({sender}, {recipient})')
        chatAddUser(sender, chat_id)
        chatAddUser(recipient, chat_id) 
        addDirectChat(sender, recipient, chat_id)
    sendMessage(sender, message, chat_id)

