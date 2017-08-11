from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkLicense(object):

    API_BASE = f'{SPARK_API_BASE}licenses/'

    def __init__(self id, name, totalUnits, consumedUnits):

        self._id = id
        self._name = name
        self._totalUnits = totalUnits
        self._consumedUnits = consumedUnits
        self._path = 'licenses'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

        @property
        def id(self):
            return self._id

        @property
        def name(self):
            return self._name

        @property
        def totalUnits(self):
            return self._totalUnits

        @property
        def consumedUnits(self):
            return self._consumedUnits

        def __repr__(self):
        return f'SparkLicense({self.id})'
