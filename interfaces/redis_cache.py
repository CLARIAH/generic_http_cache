import redis
import json
from .cache_interface import CacheInterface
from cache_item.cache_item import CacheItem

class RedisCache(CacheInterface):
    def __init__(self):
        self.client = None

    def get(self, key: str):
        value = self.client.get(key)
        if value:
            item_data = json.loads(value)
            new_cache_item = CacheItem("", "", 0)
            item = new_cache_item.from_json(item_data)
            if not item.is_expired():
                return item.value
            else:
                self.client.delete(key)
        return None

    def set(self, key: str, value: str, ttl: int = 604800):
        item = CacheItem(key, value, ttl)
        self.client.set(key, json.dumps(item.to_json()))

    def init(self, **kwargs):
        self.client = redis.Redis(
            kwargs.get('host', 'localhost'),
            kwargs.get('port', 6379),
            kwargs.get('db', 0)
        )

    def delete(self, key: str):
        self.client.delete(key)

    def show_all(self, content_type: str):
        if content_type == "json":
            return {key.decode('utf-8'): json.loads(self.client.get(key).decode('utf-8')) for key in self.client.keys('*')}

    def clear(self):
        self.client.flushdb()