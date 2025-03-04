from datetime import datetime, timedelta, timezone

class CacheItem:
    def __init__(self, key: str, value: str, ttl: int):
        self.key = key
        self.value = value
        self.expiry = datetime.now(timezone.utc) + timedelta(seconds=ttl)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expiry

    def to_json(self):
        return {
            "key": self.key,
            "value": self.value,
            "expiry": self.expiry.isoformat()
        }

    def from_json(self, data):
        self.key = data["key"]
        self.value = data["value"]
        self.expiry = datetime.fromisoformat(data["expiry"])
        return self