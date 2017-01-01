from .base import SparkBase
from ..constants import SPARK_API_BASE


class SparkRole(SparkBase):

    ''' Cisco Spark Role Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param \**kwargs: All standard Spark API properties for a Role
    '''

    API_BASE = f'{SPARK_API_BASE}roles/'

    def __init__(self, session, id, name):

        super().__init__(session, id, 'roles')
        self._name = name

        @property
        def name(self):
            ''' Role name

            :getter: Gets the name of the role
            :type: string
            '''
            return self._name

        def delete(self):
            raise NotImplemented

        def __repr__(self):
            return f'SparkRole{self.id})'
