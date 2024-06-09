import os
import redis
from functools import wraps

REDIS_CLIENT = None

def redis_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global REDIS_CLIENT
        if REDIS_CLIENT is None:
            err = connect_to_redis()
            if err:
                return f"Unable to connect to redis due to: {err}"
        return f(*args, **kwargs)
    return decorated_function

def connect_to_redis():
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_url = f"redis://{redis_host}:{redis_port}"
    global REDIS_CLIENT
    try:
        print(f"Connecting to redis on {redis_url}...")
        REDIS_CLIENT = redis.from_url(redis_url)
        REDIS_CLIENT.ping()
        return None
    except Exception as e:
        print(f"Couldn't connect to redis due to: {str(e)}")
        REDIS_CLIENT = None
        return str(e)

@redis_connection
def get_key(key):
    global REDIS_CLIENT
    try:
        value = REDIS_CLIENT.get(key)
    except Exception as e:
        err = f"Couldn't get the key due to: {str(e)}"
        print(err)
        return err, None
        
    return None, value

@redis_connection
def set_key(key, data):
    global REDIS_CLIENT
    try:
        response = REDIS_CLIENT.set(key, data)
        print(response)
    except Exception as e:
        err = f"Couldn't set the key due to: {str(e)}"
        print(err)
        return err, None
        
    return None, response

@redis_connection
def get_length_keys():
    global REDIS_CLIENT
    keys = REDIS_CLIENT.keys("*")
    return None, len(keys)

@redis_connection
def get_all_keys():
    global REDIS_CLIENT
    keys = REDIS_CLIENT.keys("*")
    return None, keys