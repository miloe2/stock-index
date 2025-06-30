class CacheStore:
    _store = {}

    @classmethod
    def get(cls, key):
        return cls._store.get(key)

    @classmethod
    def set(cls, key, value):
        cls._store[key] = value
