import redis
from fifo_cache import FIFOCache
from lifo_cache import LIFO_Cache
from lru_cache import LRU_Cache
from mru_cache import MRU_Cache
from lfu_cache import LFU_Cache

# Initialize Redis client
client = redis.Redis(host='redis', port=6379)

# Cache size
CACHE_SIZE = 5

# Initialize caches
fifo_cache = FIFOCache(client, max_size=CACHE_SIZE)
#lifo_cache = LIFO_Cache(client, max_size=CACHE_SIZE)
#lru_cache = LRU_Cache(client, max_size=CACHE_SIZE)
# mru_cache = MRU_Cache(client, max_size=CACHE_SIZE)
lfu_cache = LFU_Cache(client, max_size=CACHE_SIZE)

def add_product_to_caches(product_id, product):
    # Add product to each cache
    fifo_cache.add_product(product_id, product)
    # lifo_cache.add_product(product_id, product)
    #lru_cache.add_product(product_id, product)
    #mru_cache.add_product(product_id, product)
    #lfu_cache.add_product(product_id, product)

if __name__ == "__main__":
    # Sample list of products to add to cache
    products = {
        "1": "Product A",
        "2": "Product B",
        "3": "Product C",
        "4": "Product D",
        "5": "Product E",
        "6": "Product F"  # This will trigger cache replacement
    }

    # Add each product to caches
    for product_id, product in products.items():
        add_product_to_caches(product_id, product)

    print("\nFIFO Cache:", fifo_cache.get_all_products()) # FIFO Cache: ['Product C', 'Product D', 'Product E', 'Product F']
    #print("LIFO Cache:", lifo_cache.get_all_products()) # LIFO Cache: ['Product A', 'Product B', 'Product C', 'Product D', 'Product F']
    #print("LRU Cache:", lru_cache.get_all_products()) # LRU Cache: ['Product B', 'Product C', 'Product D', 'Product F']
    #print("MRU Cache:", mru_cache.get_all_products()) # MRU Cache: ['Product A', 'Product B', 'Product C', 'Product D', 'Product F']
    #print("LFU Cache:", lfu_cache.get_all_products()) # LFU Cache: ['Product B', 'Product D', 'Product E', 'Product F', 'Product C']
