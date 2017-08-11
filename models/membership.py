from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkMembership(object):

    API_BASE = f'{SPARK_API_BASE}memberships/'

    def __init__(self,
                 spark,
                 id,
                 roomId,
                 personId,
                 personEmail,
                 personDisplayName,
                 personOrgId,
                 isModerator,
                 isMonitor,
                 created):

        self.spark = spark
        self._id = id
        self._roomId = roomId
        self._personId = personId
        self._personEmail = personEmail
        self._personDisplayName = personDisplayName
        self._personOrgId = personOrgId
        self._isModerator = isModerator
        self._isMonitor = isMonitor
        self._created = created
        self._path = 'memberships'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

    @property
    def id(self):
        return self._id

    @property
    def roomId(self):
        return self._roomId

    @property
    def personId(self):
        return self._personId

    @property
    def personEmail(self):
        return self._personEmail

    @property
    def personDisplayName(self):
        return self._personDisplayName

    @property
    def personOrgId(self):
        return self._personOrgId

    @property
    def isModerator(self):
        return self._isModerator

    @isModerator.setter
    def isModerator(self, val):
        assert isinstance(val, bool)
        self.spark.put(self.url, json={'isModerator': val})
        return

    @property
    def isMonitor(self):
        return self._isMonitor

    @property
    def created(self):
        return ts_to_dt(self._created)

    @property
    def path(self):
        return self._path

    @property
    def url(self):
        return self._url

    def delete(self):
        self.spark.delete(self.url)
        return

    def __repr__(self):
        return f'SparkMembership({self.id})'


class SparkTeamMembership(object):

    API_BASE = f'{SPARK_API_BASE}team/memberships/'

    def __init__(self,
                 spark,
                 id,
                 teamId,
                 personId,
                 personEmail,
                 personDisplayName,
                 personOrgId,
                 isModerator,
                 created):

        self.spark = spark
        self._id = id
        self._teamId = teamId
        self._personId = personId
        self._personEmail = personEmail
        self._personDisplayName = personDisplayName
        self._personOrgId = personOrgId
        self._isModerator = isModerator
        self._created = created
        self._path = 'team/memberships'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

    @property
    def id(self):
        return self._id

    @property
    def teamId(self):
        return self._teamId

    @property
    def personId(self):
        return self._personId

    @property
    def personEmail(self):
        return self._personEmail

    @property
    def personDisplayName(self):
        return self._personDisplayName

    @property
    def personOrgId(self):
        return self._personOrgId

    @property
    def isModerator(self):
        return self._isModerator

    @property
    def created(self):
        return ts_to_dt(self._created)

    @property
    def path(self):
        return self._path

    @property
    def url(self):
        return self._url

    def delete(self):
        self.spark.delete(self.url)
        return

    def __repr__(self):
        return f'SparkTeamMembership({self.id})'
