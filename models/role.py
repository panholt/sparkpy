from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkLicense(object):

    API_BASE = f'{SPARK_API_BASE}roles/'

    def __init__(self id, name):

        self._id = id
        self._name = name
        self._path = 'roles'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

        @property
        def id(self):
            return self._id

        @property
        def name(self):
            return self._name

        def __repr__(self):
        return f'SparkRole{self.id})'
