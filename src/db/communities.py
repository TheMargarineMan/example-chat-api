from db.__init__ import *
    
def addCommunity(comm_name: str) -> int:
    """Creates a community and returns the id for the community"""
    create_comm = """
        INSERT INTO communities (comm_name)
        VALUES (%s)
        RETURNING comm_id;
    """
    return exec_commit_one(create_comm, (comm_name,))[0]

def getCommunity(comm_id: int) -> tuple:
    """Gets community details given an id"""
    get_comm = """
        SELECT * FROM communities
        WHERE comm_id = %s
    """
    return exec_get_one(get_comm)

def getCommunities() -> list:
    """Returns all existing communities"""
    get_comms = """
        SELECT * FROM communities
    """
    return exec_get_all(get_comms)

def commAddUser(user_id: int, comm_id: int) -> None:
    """Creates a relation between a community and user"""
    add_user = """
        INSERT INTO comm_users
        (user_id, comm_id)
        VALUES (%s, %s);
    """
    exec_commit(add_user, (user_id, comm_id))

def commDelUser(user_id: int, comm_id: int) -> None:
    """Deletes a relation between a community and user"""
    del_user = """
        DELETE FROM comm_users
        WHERE (user_id, comm_id) = (%s, %s)
    """
    exec_commit(del_user, (user_id, comm_id))

def commGetUsers(comm_id: int) -> list:
    """Gets all the users that are in a community"""
    get_users = """
        SELECT users.user_id, users.username FROM comm_users
        INNER JOIN users
        ON users.user_id = comm_users.user_id
        WHERE comm_id = %s
    """
    result = exec_get_all(get_users, (comm_id,))
    return result

def userGetComms(user_id: int) -> list:
    """Gets all the communities a user is in"""
    get_comms = """
        SELECT communities.comm_id, communities.comm_name FROM comm_users
        INNER JOIN communiies
        ON communities.comm_id = comm_users.comm_id
        WHERE user_id = %s
    """
    result = exec_get_all(get_comms, (user_id,))
    return result