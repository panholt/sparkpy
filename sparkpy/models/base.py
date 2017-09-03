import logging

from abc import ABC, abstractproperty, abstractmethod
from ..session import SparkSession
from ..models.time import SparkTime
from ..utils import decode_api_id, is_uuid, is_api_id, uuid_to_api_id

log = logging.getLogger('sparkpy.base')


class SparkBase(ABC, object):

    @abstractproperty
    def API_BASE(self):
        ''' Returns the base URL for the resource
        '''

    @abstractproperty
    def PROPERTIES(self):
        ''' Return a dict of SparkProperties
            representing the properties of parent class
        '''
        pass

    def __init__(self, *args, **kwargs):
        self._id = kwargs['id']
        self._path = kwargs.pop('path')
        self._parent = kwargs.pop('parent', None)
        self._uuid = None
        self._loaded = False
        self._loaded_at = None
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
        if is_api_id(val):
            self._id = val
        else:
            raise ValueError('id Must be a valid Cisco Spark API ID')

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, val):
        self._loaded = bool(val)
        return

    @property
    def loaded_at(self):
        return self._loaded_at

    @loaded_at.setter
    def loaded_at(self, val):
        self._loaded_at = val
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

    @abstractmethod
    def update(self, data):
        ''' Parent class must implement this method to accept
            a mapping of updates and process them accoringly.

            :note:
            Parent class must be able to handle updates for any
            properties defined as mutable in class.properties

            :arg data: A dictionary of updates
            :raises: `ValueError` or `AttributeError`
            :return: None
        '''
        pass

    def _fetch_data(self):
        ''' Query the Cisco Spark API to retrieve
            and load the objects properties
        '''

        with SparkSession() as s:
            resp = s.get(self.url)
            if resp.status_code == 200:
                self._load_data(resp.json())
        return

    def _load_data(self, data):
        ''' Load the data provided as **kwargs
            From the properties defined in self.PROPERTIES
        '''
        # keep a clean __setattr__
        setter = super().__setattr__
        # Check and warn for any extra kwargs
        interlopers = data.keys() - self.PROPERTIES.keys()
        for interloper in interlopers:
            log.warning('Extra kwarg provided: %s value: %s',
                        interloper, data[interloper])
        # Set all the provided kwargs
        for key, properties in self.PROPERTIES.items():
            value = data.get(key)
            if value:
                setter(key, value)
            elif properties.optional:
                setter(key, None)
            else:
                raise TypeError(f'{self} needs keyword-only argument {key}')

        # Check if all required properties are set
        if all([key in data for key in self.PROPERTIES
                if not self.PROPERTIES[key].optional]):

            # Set the _loaded flag to True and timestamp it
            setter('_loaded', True)
            setter('_loaded_at', SparkTime())
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
        ''' Hook into `__getattribute__` for lazy loading of valid attributes

             Calls `self.__getattribute__(name)` and
             if the result is `None` or `AttributeError`, and
             the `name` is present in `self.PROPERTIES.keys()` then
             query the Cisco Spark API and set the properties.

             Then calls `self.__getattribute__(name)` again
             and returns the property if it found.

             If the property is still None then and it is optional then `None`
             is returned, otherwise a `TypeError` is raised


        :return: None
        :raises: `AttributeError`, `TypeError`
        '''
        # keep a clean copy of __getattribute__
        getter = super().__getattribute__

        # see if the value exists
        try:
            attr = getter(name)
        except AttributeError:
            attr = None
        # Return the attribute if it exists
        if attr is not None:  # Don't swallow bools here
            return attr
        # Check if attribute is valid
        try:
            prop = self.PROPERTIES[name]
            # Return optional and empty values
            if self.loaded and prop.optional:
                return None
        except KeyError:
            raise AttributeError(f'{self} has no attribute "{name}"')

        # Fetch and retry the getter
        try:
            log.debug('fetching data because of %s', name)
            self._fetch_data()
            return getter(name)
        except AttributeError:
            if prop.optional:
                return None
            else:
                raise TypeError(f'{self} needs keyword-only argument {key}')

    def __setattr__(self, key, value):
        setter = super().__setattr__
        if self.PROPERTIES.get(key):
            if not self.loaded:
                self._fetch_data()
            if self.PROPERTIES[key].mutable:
                self.update(**{key: value})
            else:
                raise AttributeError(f'{self}.{key} is read only')
        setter(key, value)

    def __eq__(self, other):
        if is_api_id(other):
            return self._id == other
        elif is_uuid(other):
            return uuid_to_api_id(self._id, self._path) == self._id
        else:
            return False

    def __ne__(self, other):
        if is_api_id(other):
            return self._id != other
        elif is_uuid(other):
            return uuid_to_api_id(self._id, self._path) != self._id
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


class SparkProperty(object):

    def __init__(self, prop, mutable=False, cls=None, optional=False):
        self._prop = prop
        self._mutable = mutable
        self._cls = cls
        self._optional = optional

    @property
    def prop(self):
        return self._prop

    @property
    def mutable(self):
        return self._mutable

    @property
    def cls(self):
        return self._cls

    @property
    def optional(self):
        return self._optional

    def __repr__(self):
        return f'SparkProperty("{self.prop}")'
