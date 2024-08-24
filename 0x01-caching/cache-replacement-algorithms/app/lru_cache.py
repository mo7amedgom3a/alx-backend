import redis
"""
The LRUCache class has three methods:
- add_product(product_id, product): adds a product to the cache.
- get_product(product_id): returns a product from the cache.
- get_all_products(): returns all products in the cache.

    If the cache is full, remove the least recently used item and add the new product.
    The least recently used item is the first item in the list with the key 'lru_cache'.
    lpop('lru_cache') removes and returns the first item in the list with the key 'lru_cache'.
    delete(lru_product) deletes the item with the key lru_product.
    lrem('lru_cache', 0, product_id) removes all occurrences of product_id from the list with the key 'lru_cache'.
    rpush('lru_cache', product_id) appends product_id to the list with the key 'lru_cache'.
    set(product_id, product) sets the value of product_id to product.
    get(product_id) returns the value of product_id.
    decode('utf-8') decodes the byte string to a string.
    recently used items are moved to the end of the list to mark them as recently used.
"""
class LRU_Cache:
    def __init__(self, client, max_size=5):
        self.client = client
        self.max_size = max_size

    def add_product(self, product_id, product):
        if self.client.llen('lru_cache') >= self.max_size:
            # Remove the least recently used item
            lru_product = self.client.lpop('lru_cache') # remove and return the first item in the list(recently used)
            self.client.delete(lru_product)
        
        # Add new product to cache
        self.client.rpush('lru_cache', product_id)
        self.client.set(product_id, product)
        print(f"Added {product_id} to LRU cache")

    def get_product(self, product_id):
        # Move accessed product to the end to mark it as recently used
        if self.client.exists(product_id):
            self.client.lrem('lru_cache', 0, product_id) # remove all occurrences of product_id
            self.client.rpush('lru_cache', product_id) # append product_id to the end of the list
            return self.client.get(product_id).decode('utf-8')
        return None

    def get_all_products(self):
        return [self.client.get(pid).decode('utf-8') for pid in self.client.lrange('lru_cache', 0, -1)]
