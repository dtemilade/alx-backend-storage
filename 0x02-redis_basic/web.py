#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """Track how many times a particular URL was accessed in the key"""
    @wraps(method)

    def wrapper(url):
        count_key = "count:" + url
        cached_key = "cached:" + url

        # Increment the count of URL access
        store.incr(count_key)

        # Get the cached HTML if exists
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # Fetch HTML content from URL
        html = method(url)

        # Cache the HTML with an expiration time of 10 seconds
        store.setex(cached_key, 10, html)

        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """Return the obtained HTML content of a particular URL"""
    retval = requests.get(url)
    return retval.text
