import redis
import os

from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DATABASE = os.getenv('REDIS_DATABASE')


def redis_init():
    try:
        pool = redis.ConnectionPool(host=REDIS_URL, port=REDIS_PORT)
        conn = redis.Redis(connection_pool=pool)
    except ConnectionError:
        conn = None

    return conn
