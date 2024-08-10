from psycopg_pool import ConnectionPool
import yaml
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent / "../../config/db.yml"

# Load arguments from file 
with open(_CONFIG_PATH, 'r') as config_file:
    _ARGS = yaml.load(config_file, Loader=yaml.FullLoader)

# Format arguments into acceptable format for ConnectionPool
_CONNINFO = f'host={_ARGS["host"]} ' \
+ f'port={_ARGS["port"]} ' \
+ f'dbname={_ARGS["database"]} ' \
+ f'user={_ARGS["user"]} ' \
+ f'password={_ARGS["password"]}'

_CONNPOOL = ConnectionPool(_CONNINFO, open=True)

def exec_sql_file(path):
    with _CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            with open(path, 'r') as file:
                cur.execute(file.read())
            conn.commit()

def exec_get_one(query, args={}):
    with _CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            return cur.fetchone()

def exec_get_all(query, args={}):
    with _CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            return cur.fetchall()

def exec_commit(query, args={}):
    with _CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            conn.commit()

def exec_commit_one(query, args={}):
    with _CONNPOOL.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, args)
            conn.commit()
            return cur.fetchone()