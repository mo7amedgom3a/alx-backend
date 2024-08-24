import redis
"""
The LIFOCache class has two methods:
- add_product(product_id, product): adds a product to the cache.
- get_all_products(): returns all products in the cache.

    If the cache is full, remove the most recently added item (last inserted) and add the new product.
    The most recently added item is the last item in the list with the key 'lifo_cache'.
    llen('lifo_cache') returns the length of the list with the key 'lifo_cache'.
    rpop('lifo_cache') removes and returns the last item in the list with the key 'lifo_cache'.
    delete(newest_product) deletes the item with the key newest_product.

    'its like a fifo but instead of removing the first element we remove the last element'
"""
class LIFO_Cache:
    def __init__(self, client, max_size=5):
        self.client = client
        self.max_size = max_size

    def add_product(self, product_id, product):
        if self.client.llen('lifo_cache') >= self.max_size:
            # Remove the most recently added item (last inserted)
            newest_product = self.client.rpop('lifo_cache')
            self.client.delete(newest_product)

        # Add new product to cache
        self.client.rpush('lifo_cache', product_id)
        self.client.set(product_id, product)
        print(f"Added {product_id} to LIFO cache")

    def get_all_products(self):
        return [self.client.get(pid).decode('utf-8') for pid in self.client.lrange('lifo_cache', 0, -1)]
