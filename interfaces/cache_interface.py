"""
Abstract interface, all cache classes should implement this interface.
"""
from abc import ABC, abstractmethod

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: str):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def init(self, **kwargs):
        pass

    @abstractmethod
    def show_all(self, content_type: str):
        pass

    @abstractmethod
    def clear(self):
        pass