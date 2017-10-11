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
from collections import MutableSequence
from .time import SparkTime
from json.decoder import JSONDecodeError
from ..utils import is_api_id, is_uuid


class SparkContainer(MutableSequence):
    '''
    Generator container for Cisco Spark items
    Supports list style indexing, dict style lookups of `id`, and slicing.

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

    def __init__(self, cls, params={}, parent=None, per_page=50):
        self._cls = cls
        self._params = params
        self.params['max'] = per_page
        self._parent = parent
        self._items = list()
        self._next_page = None
        self._load_items()
        self._loaded = False
        self._loaded_at = None

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
    def per_page(self):
        return self._per_page

    @property
    def next_page(self):
        return self._next_page

    def more(self, *args):
        self._load_items()
        return

    def _load_items(self):
        if self._next_page:
            resp = self.parent.session.get(self._next_page)
        else:
            resp = self.parent.session.get(self._cls.API_BASE,
                                           params=self.params)
        next_page = resp.links.get('next', {}).get('url')
        if next_page:
            self._next_page = next_page
        else:
            self._loaded = True
            self._loaded_at = SparkTime()
        self._items.extend([self.cls(parent=self.parent, **item)
                            for item in resp.json()['items']])
        return

    def __getitem__(self, idx):
        if isinstance(idx, int):
            while idx > len(self._items) and not self._loaded:
                self._load_items()
            if idx > len(self._items):
                raise IndexError('List index must be <= {0}. ({1} > {0})'.
                                 format(str(len(self._items) - 1), idx)
                                 )
            return self._items[idx]

        # Dict Style lookups
        elif isinstance(idx, str):
            if is_uuid(key):
                key = uuid_to_api_id(key, self.cls.path)
            if is_api_id(key):
                return self.cls(key, parent=self.parent)
            else:
                raise TypeError('Key must be a uuid or Spark API ID')
        # Fail!
        else:
            raise ValueError(f'{self} requires an int or {self.cls}.id')

    def __iter__(self):
        pos = 0
        while True:
            if self._loaded and pos == len(self._items) - 1:
                return
            if pos <= len(self._items) - 1:
                yield self._items[pos]
                pos += 1
            if not self._loaded:
                self.more()
                continue

    def __len__(self):
        return len(self._items)

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, idx):
        raise NotImplementedError

    def insert(self, index, value):
        raise NotImplementedError

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
        items = []
        if re_flags:
            pattern = re.compile(regexp, re_flags)
        pattern = re.compile(regexp)

        for item in self.__make_iter():
            if hasattr(item, key) and pattern.search(getattr(item, key)):
                items.append(item)
        return items

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
        items = []
        for item in self:
            if expr(item):
                items.append(item)
        return items

    def __repr__(self):
        return f'SparkContainer({self.cls})'

    def __str__(self):
        return str(self._items)

