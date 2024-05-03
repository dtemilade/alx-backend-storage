#!/usr/bin/env python3
""" 0x02. Redis basic """

import sys
import redis
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4


def replay(method: Callable):
    """  function to display the history of calls of a particular function """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])
    count = method.__self__.get(key)
    i_list = method.__self__._redis.lrange(i, 0, -1)
    o_list = method.__self__._redis.lrange(o, 0, -1)
    queue = list(zip(i_list, o_list))
    print(f"{key} was called {decode_utf8(count)} times:")
    for k, v, in queue:
        k = decode_utf8(k)
        v = decode_utf8(v)
        print(f"{key}(*{k}) -> {v}")


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ function decorator for defining a wrapper function """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res
    return wrapper

def count_calls(method: Callable) -> Callable:
    """ count how many times methods of the Cache class are called. """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ function decorator for defining a wrapper function """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def decode_utf8(b: bytes) -> str:
    """ Decoder for the methods """
    return b.decode('utf-8') if type(b) == bytes else b


class Cache:
    """ Create a Cache class """

    def __init__(self):
        """ an instance of the Redis client as a private variable """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ method that takes a data argument and returns a string. """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float]:
        """ method that take a key string argument with optional arguement """
        res = self._redis.get(key)
        return fn(res) if fn else res

    def get_str(self, data: bytes) -> str:
        """ It will automatically parametrize Cache.get Bytes to string """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ It will automatically parametrize Cache.get Bytes to integer """
        return int.from_bytes(data, sys.byteorder)
