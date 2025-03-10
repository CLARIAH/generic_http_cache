from fastapi import FastAPI, HTTPException, Query, Request
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
def proxy(request: Request, url: str = Query(...)):
    full_requested_url = str(request.url)
    full_requested_url_parsed = urlparse(full_requested_url)
    query_params = parse_qs(full_requested_url_parsed.query)
    logger.warning(f"query_params: {query_params}")

    decoded_url = unquote(url)
    parsed_url = urlparse(decoded_url)
    accept_header = query_params.get(settings.accept_header_key, [None])[0]

    if not parsed_url.scheme or not parsed_url.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL")

    cached_content = cache.get(key=decoded_url)
    if cached_content:
        return {"source": "cache", "content": cached_content}

    try:
        headers = {"Accept": accept_header} if accept_header else {}
        logger.warning(f"Requesting {decoded_url}")
        logger.warning(f"headers: {headers}")
        response = requests.get(decoded_url, headers=headers)
        response.raise_for_status()
        content = response.text
        cache.set(key=decoded_url, value=content, ttl=settings.ttl)
        return {"source": "origin", "content": content}
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/all")
def show_all(content_type: str = "json"):
    cache_contents = cache.show_all(content_type)
    total_items = len(cache_contents)
    return JSONResponse(content={"total_items": total_items, "cache_contents": cache_contents})


@app.get("/clear")
def clear_cache():
    cache.clear()
    return {"message": "Cache cleared"}