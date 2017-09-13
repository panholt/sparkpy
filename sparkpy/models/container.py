'''
sparkpy.models.container
~~~~~~~~~~~~~~
A generator like container that follows Cisco Spark's paginated responses

The container also allows implements list style lookups and slicing, as well as
dicationary style lookups with the Cisco Spark API ids. When dictionary lookups
are made, the object attributes are lazy loaded and only fetched when accessed.

Usage:
    >>> # Iterate over all rooms
    >>> for room in spark.rooms:
        ... print(room)
    >>> # Access the most recently created room
    >>> room = spark.rooms[0]
    >>> # dictionary style lookup
    >>> room = spark.rooms['...'] # Some room id
    >>> # Room is lazy loaded, so no attributes are set
    >>> room.__dict__
        {'_id': '...',
         '_loaded': False,
         '_loaded_at': None,
         '_parent': Spark("..."),
         '_path': 'rooms',
         '_uuid': '...'}
    >>> # Access an attribute to load the room's attributes
    >>> room.title
    >>> 'The title of the room'
    >>> room.__dict__
        {'_created': '2017-08-26T12:01:36.373Z',
         '_id': '...',
         '_lastActivity': '2017-08-26T15:52:27.002Z',
         '_loaded': True,
         '_loaded_at': 2017-09-03T22:58:54.245Z,
         '_parent': Spark("..."),
         '_path': 'rooms',
         '_uuid': '...',
         'creatorId': '...',
         'isLocked': None,
         'sipAddress': '...@meet.ciscospark.com',
         'teamId': None,
         'title': 'The title of the room',
         'type': 'group'}
'''

import re
from collections import deque
from .time import SparkTime
from json.decoder import JSONDecodeError
from ..utils import is_api_id, is_uuid


class SparkContainer(object):
    '''
    Generator container for Cisco Spark items
    Supports list style indexing, dict style lookups of `id`, and slicing.

    :param session: SparkSession object
    :type session: `SparkSession`
    :param cls: Class of items in container
    :param params: Any additional params to use on the generator
    :type params: dict
    :param parent: The parent of the container

    Attributes:
        _length_map (dict): Mapping to keep length hints across containers

    .. note:: Calling len or providing negative indicies
              will result in the generator being depleated.
              This could lead to excessive API calls.
    '''

    _length_map = {}

    def __init__(self, cls, params={}, parent=None, session=None):
        self._cls = cls
        self._params = params
        self._parent = parent
        self._session = session or self.parent.session

    @property
    def cls(self):
        ''' The class used for items in the container '''
        return self._cls

    @property
    def params(self):
        '''
        Any additional URL paramaters to be included when
        creating the generator.

        :type params: `dict`
        '''
        return self._params

    @property
    def parent(self):
        '''
        The parent object of the container. This is either the
        :class:`Spark <Spark>` instance,
        a :class:`SparkRoom <SparkRoom>` for :class:`SparkMembership <SparkMembership>`
        and :class:`SparkMessage <SparkMessage>` objects associated to the room,
        or a :class:`SparkTeam <SparkTeam>` for team subrooms
        '''
        return self._parent

    @property
    def session(self):
        ''' Reference to the :class:`Spark <Spark>` instance session '''
        return self._session

    @property
    def _key(self):
        if self.parent:
            return f'{self.parent.id}:{self.cls}'
        return f'{self.cls}'

    def find(self, key, regexp, re_flags=None):
        '''
        For every item within the container
        search the value of a given key for a provided query

        :param key: Search key
        :type key: str
        :param regexp: Search string, accepts regular expressions
        :type regexp: str
        :param re_flags: (Optional) Regular expression flags
        :type re_flags: re.flags
        :yields: Any items in the container matching the search.

        Usage:
            >>> # Find all rooms with 'lunch' in the title
            >>> rooms = spark.rooms.find('title', 'lunch')
            >>> # Or, a more advanced search
            >>> rooms = spark.rooms.find('title', '^.*lunch.*$', re_flags=re.I)

        '''
        if re_flags:
            pattern = re.compile(regexp, re_flags)
        pattern = re.compile(regexp)

        for item in self.__make_iter():
            if hasattr(item, key) and pattern.search(getattr(item, key)):
                yield item

    def filtered(self, expr):
        '''
        Generator returning every item in container where expr(item)

        :param expr: Expression
        :type expr: expr
        :yields: Any items in the continer where `expr(item)`

        Usage:
            >>> # Find all locked rooms
            >>> rooms = spark.rooms.filtered(lambda room: room.isLocked)
        '''
        for item in self.__make_iter():
            if expr(item):
                yield item

    def __make_iter(self):
        response = self.session.get(self._cls.API_BASE, params=self.params)
        _next = response.links.get('next', {}).get('url')
        buffer = deque(response.json()['items'])
        count = 0
        _max_count = self.__class__._length_map.get(self._key, 0)

        while buffer:
            count += 1
            if count > _max_count:
                self.__class__._length_map[self._key] = count
            if self.parent:
                yield self._cls(parent=self.parent,
                                **buffer.popleft())
            else:
                yield self._cls(parent=self.parent, **buffer.popleft())

            if not buffer and _next:
                response = self.session.get(_next)
                _next = response.links.get('next', {}).get('url')
                buffer.extend(response.json()['items'])

    def __iter__(self):
        return self.__make_iter()

    def __getitem__(self, key):

        # List style lookups
        if isinstance(key, int):
            if key >= 0:
                for count, item in enumerate(self.__make_iter()):
                    if count == key:
                        return item
                else:
                    raise IndexError(f'{self} index out of range')

            # Negative index, must traverse all items.
            else:
                _items = list(self.__make_iter())
                if abs(key) <= len(_items) + 1:
                    return _items[key]
                else:
                    raise IndexError(f'{self} index out of range')

        # Slicing
        elif isinstance(key, slice):
            _max = max(abs(key.start or 0), abs(key.stop or 0))
            _negative = any(k < 0 for k in (key.start, key.stop))
            _items = []
            for count, item in enumerate(self.__make_iter()):
                _items.append(item)
                if count == _max and not _negative:
                    return _items[key]
            if _negative and count >= _max:
                return _items[key]
            else:
                raise IndexError(f'{self} index out of range')

        # Dict Style lookups
        elif isinstance(key, str):
            if is_uuid(key):
                key = uuid_to_api_id(key, self.cls.path)
            if is_api_id(key):
                return self.cls(key, parent=self.parent)
            else:
                raise TypeError('Key must be a uuid or Spark API ID')

        # Fail!
        else:
            raise ValueError(f'{self} requires an int or {self.cls}.id')

    def __len__(self):
        if self.__class__._length_map.get(self._key):
            return self.__class__._length_map.get(self._key, 0)
        else:
            list(self.__make_iter())
            return self.__class__._length_map.get(self._key, 0)

    def __repr__(self):
        return f'SparkContainer({self.cls})'
