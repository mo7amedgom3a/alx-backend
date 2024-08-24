#!/usr/bin/python3
""" LRU Caching"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ LRU Cache system
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            if key in self.cache_data:
                """ If key exists, update item and move to end of queue"""
                self.queue.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                """ If cache is full, discard the least recently used item"""
                discard = self.queue.pop(0)  # remove first element
                del self.cache_data[discard]
                print("DISCARD: {}".format(discard))
            self.queue.append(key)  # add key to end of queue
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key in self.cache_data:
            self.queue.remove(key)  # remove key from queue
            # add key to end of queue as most recently used
            self.queue.append(key)
            return self.cache_data[key]  # return item
        return None
