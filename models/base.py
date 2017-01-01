from abc import ABC
from ..exceptions.spark_exceptions import SparkException
from ..constants import SPARK_API_BASE
from ..utils.uuid import is_api_id, is_uuid, uuid_to_api_id


class SparkBase(ABC):

    ''' Cisco Spark Base Class

        `==` and `!=` operators overridden to compare to `id`

        :param session: SparkSession object
        :type session: `SparkSession`
        :param id: Spark object `id`
        :type id: str
        :param path: Spark API path
        :type id: str
        :param parent: Spark parent object
        :type parent: str
    '''

    def __init__(self, session, _id, path, parent=None):
        self._id = _id
        self._path = path
        self._session = session

    @property
    def id(self):
        ''' Spark object `id`

            :getter: Gets the object `id`
            :type: string
        '''
        return self._id

    @property
    def path(self):
        ''' Spark API path

            :getter: Gets the path
            :type: string
        '''
        return self._path

    @property
    def url(self):
        ''' Spark API url

            :getter: Gets the url
            :type: string
        '''
        return f'{SPARK_API_BASE}{self.path}/{self.id}'

    def delete(self):
        ''' Delete the Spark API object

        :return: None
        :raises: `SparkException`
        '''
        response = self.spark.delete(self.url)
        if response.status_code != 204:
            raise SparkException(response)

    def __eq__(self, other):
        if is_api_id(other):
            return self._id == other
        elif is_uuid(other):
            return uuid_to_api_id(self._path, self._id) == self._id
        else:
            return False

    def __ne__(self, other):
        if is_api_id(other):
            return self._id != other
        elif is_uuid(other):
            return uuid_to_api_id(self._path, self._id) != self._id
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
