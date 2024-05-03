#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
import requests
import redis
from functools import wraps
import time

store = redis.Redis()


def count_url_access(method):
    """Track how many times a particular URL was accessed"""
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


def get_page(url: str) -> str:
    """Return the HTML content of a URL"""
    retval = requests.get(url)
    return retval.text


# Decorate the get_page function with count_url_access
get_page = count_url_access(get_page)
