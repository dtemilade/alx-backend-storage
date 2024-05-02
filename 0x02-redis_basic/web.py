#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """  track how many times a particular URL was accessed in the key """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ Return the obtained the HTML content of a particular URL """
    retval = requests.get(url)
    return retval.text
