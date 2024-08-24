#!/usr/bin/python3
""" LIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache defines:
      - Inherits from BaseCaching
      - Caching system
    """

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            """ If key exists, update item and move to end of queue"""
            if key in self.cache_data:
                self.cache_data[key] = item
                self.queue.remove(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    discard = self.queue.pop()  # remove last element
                    del self.cache_data[discard]
                    print("DISCARD: {}".format(discard))
                self.cache_data[key] = item
            self.queue.append(key)

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
