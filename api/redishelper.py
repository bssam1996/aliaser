import os
import redis
from functools import wraps
import logging

REDIS_CLIENT = None

def redis_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global REDIS_CLIENT
        if REDIS_CLIENT is None:
            err = connect_to_redis()
            if err:
                logging.critical(f"Unable to connect to redis due to: {err}")
                return f"Unable to connect to redis due to: {err}"
        return f(*args, **kwargs)
    return decorated_function

def connect_to_redis():
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', '6379')
    redis_url = f"redis://{redis_host}:{redis_port}"
    global REDIS_CLIENT
    try:
        logging.info(f"Connecting to redis on {redis_url}...")
        REDIS_CLIENT = redis.from_url(redis_url)
        REDIS_CLIENT.ping()
        logging.info(f"Connected to redis")
        return None
    except Exception as e:
        logging.critical(f"Couldn't connect to redis due to: {str(e)}")
        REDIS_CLIENT = None
        return str(e)

@redis_connection
def get_key(key):
    global REDIS_CLIENT
    try:
        value = REDIS_CLIENT.get(key)
    except Exception as e:
        err = f"Couldn't get the key due to: {str(e)}"
        logging.critical(err)
        return err, None
        
    return None, value

@redis_connection
def set_key(key, data):
    global REDIS_CLIENT
    try:
        response = REDIS_CLIENT.set(key, data)
        logging.info(f"Key: {key} is set with {data}")
    except Exception as e:
        err = f"Couldn't set the key due to: {str(e)}"
        logging.critical(err)
        return err, None
        
    return None, response

@redis_connection
def delete_key(key):
    global REDIS_CLIENT
    try:
        value = REDIS_CLIENT.delete(key)
        logging.info(f"Key: {key} is deleted with response {value}")
    except Exception as e:
        err = f"Couldn't get the key due to: {str(e)}"
        logging.critical(err)
        return err
    return None, value
        
    return None, value

@redis_connection
def get_length_keys():
    global REDIS_CLIENT
    keys = REDIS_CLIENT.keys("*")
    return None, len(keys)

@redis_connection
def get_all_keys():
    global REDIS_CLIENT
    try:
        keys = REDIS_CLIENT.keys("*")
    except Exception as e:
        logging.critical(f"Couldn't get all keys due to {str(e)}")
        return str(e), None
    return None, keys