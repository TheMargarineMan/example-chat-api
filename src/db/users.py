from db.__init__ import *
from datetime import *
import secrets
import string

def getUsers() -> list:
    """Returns all users in table"""
    get_users = """
        SELECT users.user_id, username
        FROM users
        WHERE NOT EXISTS (
            SELECT * FROM inactive_users
            WHERE inactive_users.user_id = users.user_id)
        ORDER BY users.user_id ASC
    """
    return exec_get_all(get_users)

def getUser(user_id: int) -> tuple:
    """Returns user with all information from this table"""
    get_user = """
        SELECT user_id, username, NOT EXISTS(
                                    SELECT * FROM inactive_users
                                    WHERE inactive_users.user_id = users.user_id)
        FROM users
        WHERE user_id = %s       
    """
    return exec_get_one(get_user, (user_id,)) 

def getUserID(username: str) -> int:
    """Returns user_id using a username"""
    get_user_id = """
        SELECT users.user_id
        FROM users
        WHERE username = %s
    """
    result = exec_get_one(get_user_id, (username,))
    return (None if (result is None) else result[0])
       
def addUser(username: str, password: str) -> int:
    """Attempts to add user with given credentials

    Returns user_id for created user
    """
    add_user = """
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        RETURNING user_id; 
    """
    return exec_commit_one(add_user, (username, password))[0]
    
def setUsername(user_id: int, new_username: str) -> None:
    """Changes username if available"""
    alter_user = """
        UPDATE users
        SET username = %s
        WHERE user_id = %s;
    """
    exec_commit(alter_user, (new_username, user_id))

def setPassword(user_id: int, new_password: str) -> None:
    """Changes password"""    
    alter_user = """
        UPDATE users
        SET password = %s
        WHERE user_id = %s;
    """
    exec_commit(alter_user, (new_password, user_id))

def nameChangeCheck(user_id: int) -> bool:
    """Checks if user can change name"""
    get_change = """
        SELECT name_change
        FROM users
        WHERE user_id = %s
    """
    date = exec_get_one(get_change, (user_id,))[0]
    if date is None:
        return True
    return date < datetime.now()

def nameChangeTimeout(user_id: int) -> None:
    """Sets next time user can change name 6 months in the future"""
    new_time = datetime.now() + timedelta(weeks = 24)
    set_change = """
        UPDATE users
        SET name_change = %s
        WHERE user_id = %s
    """
    exec_commit(set_change, (new_time, user_id))

def deactivateUser(user_id: int) -> None:
    """Adds user to deactivated users"""
    deactivateUser = """
        INSERT INTO inactive_users (user_id)
        VALUES (%s)
    """
    exec_commit(deactivateUser, (user_id,))

def checkActiveUser(user_id: int) -> bool:
    """Check if a user is deactivated"""
    checkUser = """
        SELECT (NOT EXISTS
                SELECT * FROM inactive_users
                WHERE users.user_id = inactive_users.user_id)
        FROM users
        WHERE users.user_id = %s
    """
    return exec_get_one(checkUser, (user_id,))

def passwordAuth(user_id: int, password: str) -> bool:
    """Authenticates user"""
    get_pass = """
        SELECT password FROM users
        WHERE user_id = %s
    """
    passwd = exec_get_one(get_pass, (user_id,))[0]
    return passwd == password

def genSessionKey(user_id: int) -> string:
    """Generates and returns a session key"""
    session_key = secrets.token_hex(32)
    set_key = """
        UPDATE users
        SET session_key = %s
        WHERE user_id = %s;
    """
    exec_commit(set_key, (session_key, user_id))
    return str(session_key)

def sessionAuth(user_id: int, session_key: string) -> bool:
    """Authenticates session key"""
    get_key = """
        SELECT session_key from users
        WHERE user_id = %s
    """
    auth_key = exec_get_one(get_key, (user_id,))[0]
    return session_key == auth_key
