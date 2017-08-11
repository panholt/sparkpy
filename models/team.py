from .container import SparkContainer
from .room import SparkRoom
from .membership import SparkTeamMembership
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkTeam(object):

    API_BASE = f'{SPARK_API_BASE}teams/'

    def __init__(self, spark, id, name, created, creatorId):
        self.spark = spark
        self._id = id
        self._name = name
        self._created = created
        self._creatorId = creatorId
        self._subrooms = SparkContainer(self.spark,
                                        SparkRoom,
                                        params={'teamId': self.id,
                                                # Undocumented paramater
                                                # Reduces response time a lot
                                                'sortBy': 'id'})

        self._members = SparkContainer(self.spark,
                                       SparkTeamMembership,
                                       params={'teamId': self.id})
        self._path = 'teams'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self.spark.put(self.url, json={'name': val})
        self._val = val
        return

    @property
    def created(self):
        return ts_to_dt(self._created)

    @property
    def creatorId(self):
        return self._creatorId

    @property
    def subrooms(self):
        return self._subrooms

    @property
    def members(self):
        return self._members

    @property
    def path(self):
        return self._path

    @property
    def url(self):
        return self._url

    @property
    def delete(self):
        self.spark.delete(self.url)

    def __repr__(self):
        return f'SparkTeam({self.id})'
