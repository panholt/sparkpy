from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkOrganization(object):

    API_BASE = f'{SPARK_API_BASE}organizations/'

    def __init__(self id, displayName, created):

        self._id = id
        self._displayName = displayName
        self._created = created
        self._path = 'organizations'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

        @property
        def id(self):
            return self._id

        @property
        def displayName(self):
            return self._displayName

        @property
        def created(self):
            return ts_to_dt(self._created)

        def __repr__(self):
        return f'SparkOrganization({self.id})'
