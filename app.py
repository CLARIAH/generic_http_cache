from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from urllib.parse import urlparse, unquote, parse_qs
import requests
import cache_settings as settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize the cache based on settings
cache = settings.cache_type()
cache.init(**settings.kwargs)

@app.get("/")
def index():
    return {"message": "Hello, World!"}

@app.get("/proxy")
def proxy(url: str = Query(...)):
    decoded_url = unquote(url)
    parsed_url = urlparse(decoded_url)
    query_params = parse_qs(parsed_url.query)
    accept_header = query_params.get(settings.accept_header_key, [None])[0]

    if not parsed_url.scheme or not parsed_url.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL")

    cached_content = cache.get(key=decoded_url)
    if cached_content:
        return {"source": "cache", "content": cached_content}

    try:
        headers = {"Accept": accept_header} if accept_header else {}
        response = requests.get(decoded_url, headers=headers)
        response.raise_for_status()
        content = response.text
        cache.set(key=decoded_url, value=content, ttl=settings.ttl)
        return {"source": "origin", "content": content}
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/all")
def show_all(content_type: str = "json"):
    return JSONResponse(content=cache.show_all(content_type))

@app.get("/clear")
def clear_cache():
    cache.clear()
    return {"message": "Cache cleared"}