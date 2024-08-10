from db.__init__ import *
from datetime import datetime, timedelta
from db.communities import commDelUser

def banCheck(user_id: int, comm_id: int) -> bool:
    """Checks to see if a user is banned in a community"""
    get_ban = """
        SELECT ban_until
        FROM bans
        WHERE (user_id, comm_id) = (%s, %s)
    """
    date = exec_get_one(get_ban, (user_id, comm_id))
    if date is None:
        return False
    else: 
        return date[0] > datetime.now()

def banUser(user_id: int, comm_id: int, days: int = None) -> None:
    """Bans a user for a specified amount of days from a community

    Keyword Arguments:
    user_id - The id of the user getting banned
    comm_id - The id of the community the user will get banned from
    days - The amount of days to be banned. If left blank then ban will be indefinite    
    """
    if days is None:
        new_time = datetime.max
    else:
        new_time = datetime.now() + timedelta(days)
    get_ban = """
        SELECT *
        FROM bans
        WHERE user_id = %s
    """
    if exec_get_one(get_ban, (user_id,)) is None:
        set_ban = """
            INSERT INTO bans (ban_until, user_id, comm_id)
            VALUES (%s, %s, %s);
        """
    else:
        set_ban = """
            UPDATE bans
            SET ban_until = %s
            WHERE (user_id, comm_id) = (%s, %s)
        """
    exec_commit(set_ban, (new_time, user_id, comm_id))
    commDelUser(user_id, comm_id)

def pardonUser(user_id: int, comm_id: int) -> None:
    """Removes community ban from a specified user"""
    del_ban = """
        DELETE FROM bans
        WHERE (user_id, comm_id) = (%s, %s)
    """
    exec_commit(del_ban, (user_id, comm_id))

def commGetBans(comm_id: int) -> list:
    """Returns a list of users that were banned from a community"""
    get_bans = """
        SELECT users.user_id, users.username
        FROM bans
        INNER JOIN users
        ON users.user_id = bans.user_id
        WHERE bans.comm_id = %s
    """
    return exec_get_all(get_bans, (comm_id,))

def userGetBans(user_id: int) -> list:
    """Returns a list of communities a user is banned from"""
    get_bans = """
        SELECT communities.comm_id, communities.comm_name
        FROM bans
        INNER JOIN communities
        ON communities.comm_id = bans.comm_id
        WHERE bans.user_id = %s
    """
    return exec_get_all(get_bans, (user_id,))