from flask import Flask, jsonify, request
from .swapi_client import fetch_from_swapi
from .service import apply_filters, apply_sort, apply_pagination
import os

app = Flask(__name__)

_RESERVED = {"resource", "q", "sort", "order", "page", "page_size"}
API_KEY = os.getenv("API_KEY")

def _check_api_key():
    api_key = os.getenv("API_KEY")
    if not api_key:
        return None

    key = request.headers.get("X-API-Key")
    if key != api_key:
        return jsonify({"error": "unauthorized"}), 401

    return None

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/v1/swapi", methods=["GET"])
def swapi_proxy():
    auth = _check_api_key()
    if auth:
        return auth
    resource = request.args.get("resource")
    query = request.args.get("q")
    sort_field = request.args.get("sort", "").strip()
    order = request.args.get("order", "asc").strip().lower()

    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        page = 1

    try:
        page_size = int(request.args.get("page_size", "10"))
    except ValueError:
        page_size = 10

    if not resource:
        return jsonify({"error": "resource parameter is required"}), 400

    filters = {k: v for k, v in request.args.items() if k not in _RESERVED and v}
   
# TODO: atualmente os filtros são aplicados de forma genérica para qualquer resource.
# Em uma evolução futura seria interessante validar quais campos são permitidos
# para cada tipo de recurso retornado pela SWAPI.

    params = {}
    if query:
        params["search"] = query

    try:
        data = fetch_from_swapi(resource, params)
    except Exception:
        return jsonify({"error": "failed to fetch data from swapi"}), 502
    
    cache_status = data.pop("_cache", None)

    results = data.get("results", [])
    if not isinstance(results, list):
        return jsonify({"error": "unexpected swapi response format"}), 502

    filtered = apply_filters(results, filters)
    sorted_items = apply_sort(filtered, sort_field, order)
    paged, meta = apply_pagination(sorted_items, page, page_size)

    response = {
        "resource": resource,
        "query": query,
        "filters": filters,
        "sort": sort_field or None,
        "order": order,
        "meta": meta,
        "results": paged,
    }
    resp = jsonify(response)
    if cache_status:
        resp.headers["X-Cache"] = str(cache_status).upper()
    return resp, 200
