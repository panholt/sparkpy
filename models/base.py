from abc import ABC, abstractproperty, abstractmethod
from ..session import SparkSession
from ..models.time import SparkTime
from ..utils import decode_api_id, is_uuid, is_api_id, uuid_to_api_id


class SparkBase(ABC, object):

    def __init__(self, *args, path='', parent=None, **kwargs):
        self._id = kwargs.get('id')
        self._uuid = None
        self._path = path
        self._parent = parent
        self._loaded = False
        self._fetched_at = None
        if args:
            self._load_from_id(*args)
        else:
            if self.id:
                _id = decode_api_id(self.id)
                self._uuid = _id['uuid']
                self._path = _id['path']
                self._load_data(kwargs)
            else:
                raise ValueError('A valid Spark ID is required')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        if val.startswith('Y2lzY29zcGFyazovL'):
            self._id = val
        return

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, val):
        self._loaded = bool(val)
        return

    @property
    def fetched_at(self):
        return self._fetched_at

    @fetched_at.setter
    def fetched_at(self, val):
        self._fetched_at = val
        return

    @property
    def uuid(self):
        return self._uuid

    @property
    def path(self):
        return self._path

    @property
    def parent(self):
        return self._parent

    @property
    def url(self):
        return f'https://api.ciscospark.com/v1/{self.path}/{self.id}'

    @property
    def lastActivity(self):
        if self._lastActivity:
            return SparkTime(self._lastActivity)

    @lastActivity.setter
    def lastActivity(self, val):
        self._lastActivity = val
        return

    @property
    def created(self):
        if self._created:
            return SparkTime(self._created)

    @created.setter
    def created(self, val):
        self._created = val
        return

    @abstractproperty
    def properties(self):
        ''' Return a list of properties
            for the parent class
        '''
        return []

    @abstractmethod
    def update(self, key, value):
        pass

    def _fetch_data(self):
        with SparkSession() as s:
            resp = s.get(self.url)
            if resp.status_code == 200:
                self._load_data(resp.json())

    def _load_data(self, data):
        ''' Load the data provided as **kwargs
            From the properties defined in self.properties
        '''
        setter = super().__setattr__
        for key in self.properties.keys():
            setter(key, data.get(key))
        setter('_loaded', True)
        setter('_fetched_at', SparkTime())
        return

    def _load_from_id(self, _id):
        ''' Processes the arg if provided.

            Sets self.id and self.path

            :param _id: If uuid is provided then
                        the spark apis will be queried in an attempt
                        to determine the proper type.
            :type _id: str
        '''

        if _id.startswith('Y2lzY29zcGFyazovL'):
            _id = decode_api_id(_id)
            self._uuid = _id['uuid']
            self._path = _id['path']
            self._id = _id['id']
        elif is_uuid(_id):
            # See if its a uuid
            for path in ('messages', 'rooms', 'people',
                         'memberships', 'webhooks',
                         'teams', 'teams/memberships',
                         'organizations', 'licenses'):
                self.path = path
                self._fetch_data()
                if self._loaded:
                    self._uuid = _id
                    return
            else:
                raise ValueError('Spark API ID or a UUIDv4 string required')

        return

    def delete(self):
        ''' Delete the Spark API object

            Override to raise NotImplemented if
            the parent class does not have a delete method

        :return: None
        :raises: `SparkException`
        '''
        with SparkSession() as s:
            response = s.delete(self.url)
            if response.status_code != 204:
                # TODO Exceptions
                raise Exception()

    def __getattribute__(self, name):
        getter = super().__getattribute__
        try:
            return getter(name)
        except AttributeError:
            if self.properties.get(name):
                prop = self.properties[name]
                self._fetch_data()
                try:
                    return prop['type'](getter(name))
                except AttributeError:
                    if prop['optional']:
                        return prop['type']()
                    else:
                        raise Exception(f'{name} is required on {self}')
            else:
                raise AttributeError(f'{self} has no attribute "{name}"')
        else:
            return getter(name)

    def __setattr__(self, key, value):
        setter = super().__setattr__
        if self.properties.get(key):
            if not self.loaded:
                self._fetch_data()
            if self.properties[key]['mutable']:
                self.update(**{key: value})
            else:
                raise AttributeError(f'{self}.{key} is read only')
        setter(key, value)

    def __eq__(self, other):
        if is_api_id(other):
            return self._id == other
        elif is_uuid(other):
            return uuid_to_api_id(self._path, self._id) == self._id
        else:
            return False

    def __ne__(self, other):
        if is_api_id(other):
            return self._id != other
        elif is_uuid(other):
            return uuid_to_api_id(self._path, self._id) != self._id
        else:
            return True

    def __lt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __gt__(self, other):
        return NotImplemented

    def __ge__(self, other):
        return NotImplemented

    def __hash__(self):
        return hash(self.id)
