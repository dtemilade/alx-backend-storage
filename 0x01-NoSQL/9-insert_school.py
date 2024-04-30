#!/usr/bin/env python3
""" Python function that inserts a new document in a collection
"""


def insert_school(mongo_collection, **kwargs):
    """ request for a collection
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
