import redis
"""
The FIFOCache class has two methods:
- add_product(product_id, product): adds a product to the cache.
- get_all_products(): returns all products in the cache.

    If the cache is full, remove the oldest item (first inserted) and add the new product.
    The oldest item is the first item in the list with the key 'fifo_cache'.
    llen('fifo_cache') returns the length of the list with the key 'fifo_cache'.
    lpop('fifo_cache') removes and returns the first item in the list with the key 'fifo_cache'.
    delete(oldest_product) deletes the item with the key oldest_product.
"""
class FIFOCache:
    def __init__(self, client, max_size=5):
        """initialize the cache with the client and the maximum size"""
        self.client = client
        self.max_size = max_size

    def add_product(self, product_id, product):
        """add a product to the cache"""
        if self.client.llen('fifo_cache') >= self.max_size:
            # Remove the oldest item (first inserted)
            oldest_product = self.client.lpop('fifo_cache')
            self.client.delete(oldest_product)
        
        # Add new product to cache
        self.client.rpush('fifo_cache', product_id)
        self.client.set(product_id, product)
        print(f"Added {product_id} to FIFO cache")

    def get_all_products(self):
        return [self.client.get(pid).decode('utf-8') for pid in self.client.lrange('fifo_cache', 0, -1)]

