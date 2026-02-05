from typing import Optional, Dict, Any

import requests

from .cache import TTLCache

SWAPI_BASE_URL = "https://swapi.dev/api"
_cache = TTLCache(default_ttl_seconds=300)


def _cache_key(resource: str, params: Optional[Dict[str, Any]]) -> str:
    if not params:
        return f"{resource}?"

    pairs = sorted((str(k), str(v)) for k, v in params.items())
    flat = "&".join(f"{k}={v}" for k, v in pairs)
    return f"{resource}?{flat}"


def fetch_from_swapi(resource: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    key = _cache_key(resource, params)
    cached = _cache.get(key)
    if cached is not None:
        return {"_cache": "HIT", **cached}

    url = f"{SWAPI_BASE_URL}/{resource}/"

    try:
        response = requests.get(url, params=params, timeout=4)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError("SWAPI request failed") from exc

    data = response.json()
    _cache.set(key, data)
    return {"_cache": "MISS", **data}
