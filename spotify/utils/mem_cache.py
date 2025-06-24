from django.core.cache import cache

def add_to_cache(section, key, value, max_items=100):
        
    list_key = f"jamendo:{section}:keys"
    item_key = f"jamendo:{section}:{key}"

    #we save the data    
    cache.set(item_key, value)

    # then u pdate the key list removing our own key if it existed before (duplicated, we only want it at the top )
    keys = cache.get(list_key, [])
    keys = [k for k in keys if k != key]
    keys.append(key)

    if len(keys) > max_items:
        # Remove LRU
        for old_key in keys[:-max_items]:
            cache.delete(f"jamendo:{section}:{old_key}")
        keys = keys[-max_items:]    
    cache.set(list_key, keys)