from .cache_interface import CacheInterface
from cache_item.cache_item import CacheItem
import json

class InMemoryCache(CacheInterface):
    def __init__(self):
        self.store = {}

    def get(self, key: str):
        item = self.store.get(key)
        if item and not item.is_expired():
            return item.value
        elif item and item.is_expired():
            del self.store[key]
        return None

    def set(self, key: str, value: str, ttl: int = 604800):
        self.store[key] = CacheItem(key, value, ttl)

    def init(self, **kwargs):
        pass

    def delete(self, key: str):
        if key in self.store:
            del self.store[key]

    def show_all(self, content_type: str):
        return json.dumps(self.store, default=lambda o: o.to_json(), indent=4)

    def clear(self):
        self.store.clear()