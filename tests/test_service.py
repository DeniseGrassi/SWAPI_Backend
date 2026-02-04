from src.service import apply_filters, apply_sort, apply_pagination

def test_apply_filters_simple():
    items = [
        {"name": "Luke", "gender": "male"},
        {"name": "Leia", "gender": "female"},
    ]

    result = apply_filters(items, {"gender": "male"})

    assert len(result) == 1
    assert result[0]["name"] == "Luke"

def test_apply_sort_by_name_asc():
    items = [
        {"name": "b"},
        {"name": "a"},
        {"name": "c"},
    ]

    result = apply_sort(items, "name", "asc")

    assert [i["name"] for i in result] == ["a", "b", "c"]

def test_apply_sort_by_name_desc():
    items = [
        {"name": "a"},
        {"name": "b"},
        {"name": "c"},
    ]

    result = apply_sort(items, "name", "desc")

    assert [i["name"] for i in result] == ["c", "b", "a"]

def test_apply_pagination():
    items = [{"id": i} for i in range(1, 21)]

    page_items, meta = apply_pagination(items, page=2, page_size=5)

    assert [i["id"] for i in page_items] == [6, 7, 8, 9, 10]
    assert meta["page"] == 2
    assert meta["page_size"] == 5
    assert meta["total_items"] == 20
    assert meta["total_pages"] == 4
