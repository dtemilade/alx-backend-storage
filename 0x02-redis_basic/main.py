#!/usr/bin/env python3
""" Main file """

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

i = cache._redis.lrange("{}:i".format(cache.store.__qualname__), 0, -1)
o = cache._redis.lrange("{}:o".format(cache.store.__qualname__), 0, -1)

print("i: {}".format(i))
print("o: {}".format(o))
