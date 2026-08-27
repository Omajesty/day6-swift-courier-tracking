cache_list = []
cache_size = 10


def cache_key(kind, detail):
    return kind + ":" + str(detail).strip().lower()


def cache_get(kind, detail):
    key = cache_key(kind, detail)
    for copy in cache_list:
        if copy["question"] == key:
            return copy["answer"]
    return None


def cache_put(kind, detail, answer):
    cache_drop(kind, detail)
    cache_list.append({
        "question": cache_key(kind, detail),
        "answer": answer,
    })
    if len(cache_list) > cache_size:
        cache_list.pop(0)


def cache_drop(kind, detail):
    key = cache_key(kind, detail)
    kept = []
    for copy in cache_list:
        if copy["question"] != key:
            kept.append(copy)
    cache_list[:] = kept


def cache_wipe(code, city, status, old_status=None):
    # If a parcel changed, drop stale cache entries.
    cache_drop("parcel", code)
    if city:
        cache_drop("city", city)
    cache_drop("status", status)
    if old_status and old_status != status:
        cache_drop("status", old_status)
