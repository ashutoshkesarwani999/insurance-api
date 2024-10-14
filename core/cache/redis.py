from redis import Redis
from functools import lru_cache
from core.config import config
@lru_cache()
def get_redis():
    return Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)

def get_redis_client():
    return get_redis()
