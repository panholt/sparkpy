from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkMessage(object):

    API_BASE = f'{SPARK_API_BASE}messages/'

    def __init__(self,
                 spark,
                 created,
                 id,
                 personEmail,
                 personId,
                 roomId,
                 roomType,
                 text,
                 html=None,
                 markdown=None,
                 files=[]):

        self._created = created
        self._html = html
        self._id = id
        self._markdown = markdown
        self._personEmail = personEmail
        self._personId = personId
        self._roomId = roomId
        self._roomType = roomType
        self._text = text
        self._files = files
        self._path = 'messages'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

    @property
    def id(self):
        return self._id

    @property
    def html(self):
        return self._html

    @property
    def created(self):
        return ts_to_dt(self._created)

    @property
    def markdown(self):
        return self._markdown

    @property
    def personEmail(self):
        return self._personEmail

    @property
    def personId(self):
        return self._personId

    @property
    def roomId(self):
        return self._roomId

    @property
    def roomType(self):
        return self._roomType

    @property
    def text(self):
        return self._text

    @property
    def url(self):
        return self._url

    @property
    def path(self):
        return self._path

    @property
    def files(self):
        return self._files

    def delete(self):
        self.spark.delete(self.url)
        return

    def __repr__(self):
        return f'SparkMessage({self.id})'
