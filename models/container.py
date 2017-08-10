from datetime import datetime
from collections import deque
from ..utils.uuid import is_api_id


class SparkContainer(object):
    ''' Generic Generator Container '''

    def __init__(self, spark, klass, params={}):
        self.spark = spark
        self._klass = klass
        self._created = datetime.now()
        self._generator = self._make_generator()
        self._items = deque()
        self._finished = False
        self._params = params

    @property
    def klass(self):
        return self._klass

    @property
    def created(self):
        return self._created

    def __getitem__(self, key):
        # List style lookups
        if isinstance(key, int):
            while len(self._items) - 1 <= key and not self._finished:
                try:
                    self._generator.__next__()
                except StopIteration:
                    if len(self._items) - 1 < key or not self._items:
                        raise IndexError(f'{self} index out of range')
                    else:
                        return self._items[key]

            return self._items[key]
        # Dict sytle lookups
        elif isinstance(key, str) and is_api_id(key):
            items = [item for item in self._items if item.id == key]
            if items:
                return items[0]
            else:
                resp = self.spark.get(self._klass.API_BASE + key)
                return self._klass(self.spark, **resp.json())
        else:
            raise TypeError('Indices must be an int or Spark API ID')

    def _make_generator(self, params={}):
        assert isinstance(params, dict)
        response = self.spark.get(self._klass.API_BASE, params=self._params)
        data = response.json()
        items = deque(data.get('items', []))
        while items:
            item = self._klass(self.spark, **items.popleft())
            self._items.append(item)
            yield item

            if not items:
                if response.links.get('next'):
                    response = self.spark.get(response.links['next']['url'])
                    items.extend(response.json()['items'])
                else:
                    self._finished = True
                return

    def __repr__(self):
        return f'SparkContainer({self.klass})'
