from interfaces import in_mem_cache, redis_cache

cache_type = in_mem_cache.InMemoryCache # or redis_cache.RedisCache
# cache_type = redis_cache.RedisCache # or in_mem_cache.InMemoryCache
kwargs = {
    'host': 'redis',
    'port': 6379,
    'db': 0
}
ttl = 604800 # (1 week)
accept_header_key = "accept"
