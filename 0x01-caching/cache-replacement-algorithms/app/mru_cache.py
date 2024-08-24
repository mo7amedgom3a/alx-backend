import redis
"""
The MRUCache class has three methods:
- add_product(product_id, product): adds a product to the cache.
- get_product(product_id): returns a product from the cache.
- get_all_products(): returns all products in the cache.

    If the cache is full, remove the most recently used item and add the new product.
    The most recently used item is the last item in the list with the key 'mru_cache'.
    llen('mru_cache') returns the length of the list with the key 'mru_cache'.
    rpop('mru_cache') removes and returns the last item in the list with the key 'mru_cache'.
    delete(mru_product) deletes the item with the key mru_product.
    lrem('mru_cache', 0, product_id) removes all occurrences of product_id from the list with the key 'mru_cache'.
    rpush('mru_cache', product_id) appends product_id to the list with the key 'mru_cache'.
    set(product_id, product) sets the value of product_id to product.
    get(product_id) returns the value of product_id.
    decode('utf-8') decodes the byte string to a string.
    recently used items are moved to the end of the list to mark them as most recently used.

    the cache look like
    mru_cache = {product_id1, product_id2, product_id3} --> list
    
"""
class MRU_Cache:
    def __init__(self, client, max_size=5):
        self.client = client
        self.max_size = max_size

    def add_product(self, product_id, product):
        if self.client.llen('mru_cache') >= self.max_size:
            # Remove the most recently used item
            mru_product = self.client.rpop('mru_cache')
            self.client.delete(mru_product)

        # Add new product to cache
        self.client.rpush('mru_cache', product_id)
        self.client.set(product_id, product)
        print(f"Added {product_id} to MRU cache")

    def get_product(self, product_id):
        # Move accessed product to the end to mark it as most recently used
        if self.client.exists(product_id):
            self.client.lrem('mru_cache', 0, product_id)
            self.client.rpush('mru_cache', product_id)
            return self.client.get(product_id).decode('utf-8')
        return None

    def get_all_products(self):
        return [self.client.get(pid).decode('utf-8') for pid in self.client.lrange('mru_cache', 0, -1)]
