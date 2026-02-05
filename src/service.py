from typing import Any, Dict, List, Tuple


def _normalize(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _is_scalar(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool))


def apply_filters(items: List[Dict[str, Any]], filters: Dict[str, str]) -> List[Dict[str, Any]]:

    if not filters:
        return items

    out: List[Dict[str, Any]] = []
    for it in items:
        ok = True
        for key, expected in filters.items():
            if key not in it:
                ok = False
                break

            val = it.get(key)

            
            if not _is_scalar(val):
                ok = False
                break

            if _normalize(val) != _normalize(expected):
                ok = False
                break

        if ok:
            out.append(it)
    return out


def apply_sort(items: List[Dict[str, Any]], sort_field: str, order: str) -> List[Dict[str, Any]]:
    if not sort_field:
        return items

    reverse = (order or "").lower() == "desc"

    def key_fn(it: Dict[str, Any]):
        val = it.get(sort_field)
        if val is None:
            return (1, "")
        
        return (0, _normalize(val))

    return sorted(items, key=key_fn, reverse=reverse)


def apply_pagination(items: List[Dict[str, Any]], page: int, page_size: int) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    if page_size > 50:
        page_size = 50

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    sliced = items[start:end]
    meta = {
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "total_pages": (total + page_size - 1) // page_size if page_size else 0,
    }
    return sliced, meta
