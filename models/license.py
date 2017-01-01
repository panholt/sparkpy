from .base import SparkBase
from ..constants import SPARK_API_BASE


class SparkLicense(SparkBase):

    ''' Cisco Spark License Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param \**kwargs: All standard Spark API properties for a License
    '''

    API_BASE = f'{SPARK_API_BASE}licenses/'

    def __init__(self, session, id, name, totalUnits, consumedUnits):

        super().__init__(session, id, 'licenses')
        self._name = name
        self._totalUnits = totalUnits
        self._consumedUnits = consumedUnits

        @property
        def name(self):
            ''' License name

            :getter: Gets the name of the license
            :type: string
            '''
            return self._name

        @property
        def totalUnits(self):
            ''' Total units 

            :getter: Gets the total number of licenses available
            :type: int
            '''
            return self._totalUnits

        @property
        def consumedUnits(self):
            ''' Consumed units

            :getter: Gets the total number of licenses used
            :type: int
            '''
            return self._consumedUnits

        def delete(self):
            raise NotImplemented

        def __repr__(self):
            return f'SparkLicense({self.id})'
