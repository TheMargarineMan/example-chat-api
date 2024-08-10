from db.__init__ import *
from datetime import *

def addMessage(message: str, user_id: int, chat_id: int) -> int:
    """Creates a message and returns an id"""
    insert_message = f"""
        INSERT INTO messages (message, timestamp, user_id, chat_id)
        VALUES (%s, NOW(), %s, %s)
        RETURNING msg_id;
    """
    return exec_commit_one(insert_message, (message, user_id, chat_id))[0]

def delMessage(msg_id: int) -> None:
    """Deletes a message with specified msg_id."""
    delete_message = """
        DELETE FROM messages
        WHERE msg_id = %s
    """
    exec_commit(delete_message, (msg_id,))

def editMessage(msg_id: int, new_message: str) -> None:
    """Replaces text in existing message and sets edited to True"""
    edit_message = """
        UPDATE messages
        SET message = %s, edited = True
        WHERE msg_id = %s
    """
    exec_commit(edit_message, (new_message, msg_id))

def getChatHistory(chat_id: int, args: dict = {}) -> list:
    """Gets a list of all messages that were sent in a chat room"""

    # TODO: Input mentions searching in here
    # TODO: Input unreads searching in here?
    
    
    limit = args.get('limit', '50')

    sql_args = [chat_id]
    
    get_history = """
        SELECT * FROM messages
        WHERE chat_id = %s
    """
    
    for arg in args.keys():
        if arg == 'contains':
            get_history += '\nAND LOWER(message) LIKE \'%%\' || %s || \'%%\''
        elif arg == 'before':
            get_history += '\nAND timestamp < %s'
        elif arg == 'after':
            get_history += '\nAND timestamp > %s'
        elif arg == 'user':
            get_history += '\nAND user_id = %s'
        else:
            continue
        sql_args.append(args.get(arg))
    
    get_history += """
        ORDER BY timestamp DESC
        LIMIT %s;
    """
    sql_args.append(limit)
    return exec_get_all(get_history, sql_args)
    
def readMessage(user_id: int, msg_id: int) -> None:
    """Deletes message and user relation from unread_messages"""
    del_message = """
        DELETE FROM unread_messages
        WHERE (user_id, msg_id) = (%s, %s)
    """
    exec_commit(read_message, (user_id, msg_id))

def generateUnreads(msg_id: int, user_list: list) -> None:
    """Generates an list of unreads for the users in the list"""
    gen_unread = """
        INSERT INTO unread_messages (msg_id, user_id)
        VALUES (%s, %s);
    """
    for user in user_list:
        exec_commit(gen_unread, (msg_id, user))

def userGetUnreads(user_id: int) -> list:
    """Returns a list for messages that are not read by the user"""
    get_unreads = """
        SELECT      messages.msg_id, 
                    messages.message, 
                    messages.edited, 
                    messages.timestamp, 
                    messages.user_id, 
                    messages.chat_id 
        FROM unread_messages
        INNER JOIN messages
        ON messages.msg_id = unread_messages.msg_id
        WHERE unread_messages.user_id = %s
        ORDER BY timestamp DESC
    """
    return exec_get_all(get_unreads, (user_id,))

def userGetUnreadCount(user_id: int) -> int:
    """Returns the count of unread messages instead of list"""
    get_unread_count = """
        SELECT COUNT(*) FROM unread_messages
        WHERE unread_messages.user_id = %s
    """
    return exec_get_one(get_unread_count, (user_id,))[0]

def userGetUnreadsChat(user_id: int, chat_id: int) -> list:
    """Returns a list of unread messages in a chat"""
    get_unreads = """
        SELECT      messages.msg_id, 
                    messages.message, 
                    messages.edited, 
                    messages.timestamp, 
                    messages.user_id, 
                    messages.chat_id 
        FROM unread_messages
        INNER JOIN messages
        ON messages.msg_id = unread_messages.msg_id
        WHERE (unread_messages.user_id, chat_id) = (%s, %s)
        ORDER BY messages.timestamp DESC
    """
    return exec_get_all(get_unreads, (user_id, chat_id))

def userGetUnreadChatCount(user_id: int, chat_id: int) -> int:
    """Returns the number of unread messages a user has in a chat"""
    get_unread_count = """
        SELECT COUNT(*) FROM unread_messages
        INNER JOIN messages
        ON messages.msg_id = unread_messages.msg_id
        WHERE (unread_messages.user_id, chat_id) = (%s, %s)
    """
    return exec_get_one(get_unread_count, (user_id, chat_id))[0]

def generateMentions(msg_id: int, user_list: list) -> None:
    """Generates a list of mentions for the users in a list"""
    gen_mention = """
        INSERT INTO mentions            
        (msg_id, user_id)
        VALUES (%s, %s);
    """
    for user in user_list:
        exec_commit(gen_mention, (msg_id, user))

def userGetMentions(user_id: int) -> list:
    """Returns all messages that mentions a user"""
    get_mentions = """        
        SELECT      messages.msg_id, 
                    messages.message, 
                    messages.edited, 
                    messages.timestamp, 
                    messages.user_id, 
                    messages.chat_id 
        FROM mentions
        INNER JOIN messages
        ON messages.msg_id = mentions.msg_id
        WHERE mentions.user_id = %s
        ORDER BY messages.timestamp DESC
    """
    return exec_get_all(get_mentions, (user_id,))

def queryChat(chat_id: int, query: str) -> list:
    """Returns all messages that contain a search term"""
    get_messages = """
        SELECT * FROM messages
        WHERE to_tsvector(message) @@ to_tsquery(%s)
        AND chat_id = %s
        ORDER BY timestamp DESC
    """
    return exec_get_all(get_messages, (query, chat_id))

def activitySummary(chat_id: int) -> int:
    """Returns the average message count in the last 30 days"""
    get_average = """
        SELECT COUNT(*)/30.0 FROM messages
        WHERE chat_id = %s
        AND timestamp > NOW() - INTERVAL '30 day'
        AND LENGTH(message) >= 5
    """
    return exec_get_one(get_average, (chat_id,))[0]

def modQuery(comm_id: int, date_start: datetime, date_end: datetime):
    """Takes a range of times and searches a community for all messages
    sent by suspended users in the time range """
    get_messages = """
        SELECT  messages.msg_id,
                messages.chat_id,
                users.username,
                messages.message,
                messages.edited,
                messages.timestamp
        FROM messages
        INNER JOIN users
        ON users.user_id = messages.user_id
        INNER JOIN chats
        ON chats.chat_id = messages.chat_id
        WHERE chats.comm_id = %s
        AND messages.timestamp between %s and %s
        AND EXISTS(
            SELECT * FROM bans
            WHERE (user_id, comm_id) = (users.user_id, %s)    
        )
        ORDER BY messages.timestamp DESC;
    """
    return exec_get_all(get_messages, (comm_id, date_start, date_end, comm_id))