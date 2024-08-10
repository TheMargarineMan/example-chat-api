from db.__init__ import *

def addChat(chat_name: str, comm_id: int = None) -> int:
    """Constructs a new chatroom with given name and comm_id"""
    create_chat = """
        INSERT INTO chats (chat_name, comm_id)
        VALUES (%s, %s)
        RETURNING chat_id;
    """
    return exec_commit_one(create_chat, (chat_name, comm_id))[0]    

def getChat(chat_id: int) -> tuple:
    """Gets a chat with the specified ID"""
    get_chat = """
        SELECT * FROM chats
        WHERE chat_id = %s
    """
    return exec_get_one(get_chat, (chat_id,))

def getChats() -> list:
    """Returns all chats"""
    get_chats = """
        SELECT * FROM chats
    """
    return exec_get_all(get_chats)

def addDirectChat(user_one: int, user_two: int, chat_id: int):
    """Adds chat to direct_chats table with users"""
    add_chat = """
        INSERT INTO direct_chats
        (user_one, user_two, chat_id)
        VALUES (%s, %s, %s)
    """
    exec_commit(add_chat, (user_one, user_two, chat_id))

def getDirectChats(user_id: int) -> list:
    """Gets a list of all direct chats a user is in"""
    get_chats = """
        SELECT direct_chats.chat_id FROM direct_chats
        INNER JOIN chats
        ON direct_chats.chat_id = chats.chat_id
        WHERE user_one = %s 
        OR user_two = %s
    """
    # Uses list comprehension in order to extract integer from typically returbed tuple
    return [n[0] for n in exec_get_all(get_chats, (user_id, user_id))]

def getDirectChat(user_one: int, user_two: int):
    """Gets the direct chat between two users"""
    get_chat = """
        SELECT chat_id 
        FROM direct_chats
        WHERE (user_one, user_two) = (%s, %s)
        OR (user_two, user_one) = (%s, %s)
    """
    
    return exec_get_one(get_chat, (user_one, user_two, user_one, user_two))[0]
        
def chatGetComm(chat_id: int) -> tuple:
    """Returns the information to the community the chat is in."""
    get_comm = """
        SELECT * FROM chats
        INNER JOIN communities
        ON chats.comm_id = communities.comm_id
        WHERE chat_id = %s
    """
    return exec_get_one(get_comm, (chat_id,))

def commGetChats(comm_id: int) -> list:
    """Returns all the chats in a community"""
    get_chats = """
        SELECT chat_id, chat_name FROM chats
        WHERE comm_id = %s
    """
    return exec_get_all(get_chats, (comm_id,))

def chatAddUser(user_id: int, chat_id: int) -> None:
    """This creates a relation between a user and a chatroom"""
    add_user = """
        INSERT INTO chat_users (user_id, chat_id)
        VALUES (%s, %s);
    """
    exec_commit(add_user, (user_id, chat_id))

def chatDelUser(user_id: int, chat_id: int) -> None:
    """Removes an existing relation between a user and a chatroom"""
    remove_user = """
        DELETE FROM chat_users
        WHERE user_id = %s
        AND chat_id = %s;
    """
    exec_commit(remove_user, (user_id, chat_id))

def chatGetUsers(chat_id: int) -> list:
    """Returns a list of all users in a chatroom"""
    get_users = """
        SELECT users.user_id, users.username FROM chat_users
        INNER JOIN users
        ON users.user_id = chat_users.user_id
        WHERE chat_id = %s
    """
    result = exec_get_all(get_users, (chat_id,))
    return result

def userGetChats(user_id: int) -> list:
    """Returns a list of all the chats a user is in"""
    get_chats = """
        SELECT chats.chat_id, chats.chat_name FROM chat_users
        INNER JOIN chats
        ON chats.chat_id = chat_users.chat_id
        WHERE user_id = %s
    """
    result = exec_get_all(get_chats, (user_id,))
    return result

