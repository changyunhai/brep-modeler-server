import datetime
import threading
import copy


class CacheItem:
    def __init__(self, data=None):
        self.timestamp = datetime.datetime.now()
        self.date = data
        return


class Cache(dict):
    def __init__(self):
        pass

    def set(self, key, data):
        self.heartbeat(key)
        item = super().get(key)
        if item is None:
            self[key] = item = CacheItem()
        item.data = data

    def get(self, key):
        self.heartbeat(key)
        item = super().get(key)
        if item is not None:
            return item.data
        return None

    def heartbeat(self, key):
        item = super().get(key)
        if item is not None:
            item.timestamp = datetime.datetime.now()
        pass


gCache = Cache()
_cacheValidateDelta = datetime.timedelta(hours=2)  # 设置缓存失效时间


# -------------clear cache

def _clearCache():
    global timer
    global gCache
    timer = threading.Timer(2, _clearCache)
    timer.start()

    #######
    now = datetime.datetime.now()
    cacheKeys = list(gCache.keys())
    for key in cacheKeys:
        cacheItem = gCache[key]
        if now - cacheItem.timestamp > _cacheValidateDelta:
            del gCache[key]
    pass


timer = threading.Timer(0.5, _clearCache)
timer.start()
