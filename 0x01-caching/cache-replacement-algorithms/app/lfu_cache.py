import redis
"""
The LFUCache class has three methods:
- add_product(product_id, product): adds a product to the cache.
- get_product(product_id): returns a product from the cache.
- get_all_products(): returns all products in the cache.

    If the cache is full, remove the least frequently used item and add the new product.
    The least frequently used item is the item with the lowest frequency count in the hash with the key 'lfu_frequency'.
    scard('lfu_cache') returns the cardinality (number of elements of the set) of the set with the key 'lfu_cache'.
    hvals('lfu_frequency') returns the values of the hash with the key 'lfu_frequency'.
    hget('lfu_frequency', min_freq) returns the key with the value min_freq in the hash 'lfu_frequency'.
    delete(lfu_product) deletes the item with the key lfu_product.
    srem('lfu_cache', lfu_product) removes lfu_product from the set with the key 'lfu_cache'.
    hdel('lfu_frequency', lfu_product) deletes the key lfu_product from the hash 'lfu_frequency'.
    sadd('lfu_cache', product_id) adds product_id to the set with the key 'lfu_cache'.
    set(product_id, product) sets the value of product_id to product.
    hset('lfu_frequency', product_id, 1) sets the frequency count of product_id to 1.
    get(product_id) returns the value of product_id.
    decode('utf-8') decodes the byte string to a string.
    hincrby('lfu_frequency', product_id, 1) increments the frequency count of product_id by 1.

    the cache look like
    lfu_cache = {product_id1, product_id2, product_id3} --> set
    lfu_frequency = {product_id1: 1, product_id2: 2, product_id3: 3} --> hash
"""
class LFU_Cache:
    def __init__(self, client, max_size=5):
        self.client = client
        self.max_size = max_size

    def add_product(self, product_id, product):
        if self.client.scard('lfu_cache') >= self.max_size:
            # Find and remove the least frequently used item
            min_freq = min(self.client.hvals('lfu_frequency'))
            lfu_product = self.client.hget('lfu_frequency', min_freq) # returns the key with the value min_freq
            self.client.delete(lfu_product)
            self.client.srem('lfu_cache', lfu_product) # remove lfu_product from the set
            self.client.hdel('lfu_frequency', lfu_product) # delete lfu_product from the hash

        # Add new product to cache
        self.client.sadd('lfu_cache', product_id)
        self.client.set(product_id, product)
        self.client.hset('lfu_frequency', product_id, 1)
        print(f"Added {product_id} to LFU cache")

    def get_product(self, product_id):
        if self.client.exists(product_id):
            # Increase frequency count
            self.client.hincrby('lfu_frequency', product_id, 1)
            return self.client.get(product_id).decode('utf-8')
        return None

    def get_all_products(self):
        return [self.client.get(pid).decode('utf-8') for pid in self.client.smembers('lfu_cache')]
