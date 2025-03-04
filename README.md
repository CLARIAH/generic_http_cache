# Generic Cache
Generic cache is a caching server over http, the url sent to the server is checked for existence in the 
key value store.

### How to use
The `cache_settings.py` file contains the configuration for the server. 
```python
cache_type = in_mem_cache.InMemoryCache # or redis_cache.RedisCache
kwargs = {
    'host': 'redis',
    'port': 6379,
    'db': 0
}
ttl = 604800 # (1 week)
accept_header_key = "accept"
```
  - The `cache_type` (*required*) variable can be set to either `in_mem_cache.InMemoryCache` or `redis_cache.RedisCache`.
  - The `ttl` (*required*) is the time to live for the key in seconds.
  - The `accept_header_key` (*required*) is the url parameter we are going to use to when fetching from origin as the http accept header.
  - Others are optional and can be set as required. Like the `kwargs` variable which is a dictionary of the connection parameters for the redis server.

**NOTE** The corresponding `interface` for the cache type should *"know"* how to handle the required config items. 

### Running the server
To run the server, you can use the following command:
  - For dev build
```bash
docker compose -f docker-compose.yml up -d
```

  - For prod build
```bash
docker compose up -d
```

