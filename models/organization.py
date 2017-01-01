from .base import SparkBase
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkOrganization(SparkBase):

    ''' Cisco Spark Organization Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param \**kwargs: All standard Spark API properties for a Organization
    '''

    API_BASE = f'{SPARK_API_BASE}organizations/'

    def __init__(self, session, id, displayName, created):

        super().__init__(session, id, 'organizations')
        self._displayName = displayName
        self._created = created

    @property
    def displayName(self):
        ''' Org display name

            :getter: Gets the `displayName` of the org
            :type: string
        '''
        return self._displayName

    @property
    def created(self):
        ''' Org creation time

            :getter: returns datetime object of org creation time
            :type: datetime.datetime
        '''
        return ts_to_dt(self._created)

    def delete(self):
            raise NotImplemented

    def __repr__(self):
        return f'SparkOrganization({self.id})'
