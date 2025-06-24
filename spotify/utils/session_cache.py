from collections import OrderedDict

def add_to_session_cache(session, section, key,value, max_items=20):
    cache = session.get("jamendo",{}).get(section, OrderedDict())
    #if cache is NOT an ordered Dict we initialize it
    if not isinstance(cache, OrderedDict):
        cache = OrderedDict(cache)
    
    #remove if the item exists (avoid duplicating the item)
    cache.pop(str(key), None)
    #Add the item. If it existed before it will be at the top now as OrderedDict mantains order
    cache[str(key)]=value
    
    #if cache is longer than the max allowed, remove the oldest items until we're good on length
    while len(cache) > max_items:
        cache.popitem(last=False)
    
    
    session.setdefault("jamendo", {})[section] = cache
    session.modified = True


