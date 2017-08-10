from .message import SparkMessage
from .membership import SparkMembership
from .container import SparkContainer
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkRoom(object):

    API_BASE = f'{SPARK_API_BASE}rooms/'

    def __init__(self,  # *args, **kwargs):
                 spark,
                 id,
                 title,
                 type,
                 isLocked,
                 lastActivity,
                 created,
                 creatorId,
                 sipAddress=None,
                 teamId=None):

        self.spark = spark
        self._id = id
        self._title = title
        self._type = type
        self._isLocked = isLocked
        self._lastActivity = lastActivity
        self._created = created
        self._creatorId = creatorId
        self._sipAddress = sipAddress
        self._teamId = teamId
        self._path = 'rooms'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'
        self._messages = SparkContainer(self.spark,
                                        SparkMessage,
                                        params={'roomId': self.id})
        self._members = SparkContainer(self.spark,
                                       SparkMembership,
                                       params={'roomId': self.id})

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        assert isinstance(value, str)
        assert len(value) > 0
        self.spark.put(self.path, json={'title': value})
        self._title = value
        return

    @property
    def type(self):
        return self._type

    @property
    def isLocked(self):
        return self._isLocked

    @isLocked.setter
    def isLocked(self, value):
        assert isinstance(value, bool)
        # TODO this.
        self._isLocked = value

    @property
    def lastActivity(self):
        return ts_to_dt(self._lastActivity)

    @property
    def created(self):
        return ts_to_dt(self._created)

    @property
    def creatorId(self):
        return self._creatorId

    @property
    def sipAddress(self):
        return self._sipAddress

    @property
    def teamId(self):
        return self._teamId

    @property
    def path(self):
        return self._path

    @property
    def messages(self):
        return self._messages

    def __repr__(self):
        return f'SparkRoom({self.id})'
