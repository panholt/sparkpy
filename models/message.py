from .base import SparkBase
from .file import SparkFile
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkMessage(SparkBase):

    ''' Cisco Spark Message Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param parent: `SparkRoom` object of parent room
        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = f'{SPARK_API_BASE}messages/'

    def __init__(self,
                 session,
                 id,
                 created,
                 personEmail,
                 personId,
                 roomId,
                 roomType,
                 text,
                 html=None,
                 markdown=None,
                 files=[],
                 parent=None):

        super().__init__(session, id, 'messages', parent=parent)
        self._created = created
        self._html = html
        self._markdown = markdown
        self._personEmail = personEmail
        self._personId = personId
        self._roomId = roomId
        self._roomType = roomType
        self._text = text
        self._files = files

    @property
    def html(self):
        ''' HTML encoded message body

            :getter: Get the HTML encoded message body
            :type: string
            '''
        return self._html

    @property
    def created(self):
        ''' Message creation time

            :getter: returns datetime object of message creation time
            :type: datetime.datetime
        '''
        return ts_to_dt(self._created)

    @property
    def markdown(self):
        ''' Markdown formatted message body

            Returns `text` property if `markdown` property does not exist

            :getter: Get the Markdown formatted message body
            :type: string
        '''
        return self._markdown or self._text

    @property
    def personEmail(self):
        ''' email address of message creator

            :getter: email address of message creator
            :type: str
        '''
        return self._personEmail

    @property
    def personId(self):
        ''' `id` of message creator

            :getter: `id` of message creator
            :type: str
        '''
        return self._personId

    @property
    def roomId(self):
        ''' `roomId` of room where message resides

            :getter: `roomId` of Spark Room
            :type: str
        '''
        return self._roomId

    @property
    def roomType(self):
        ''' Type of room where message resides.

            :getter: either 'direct' or 'group'
            :type: str
        '''
        return self._roomType

    @property
    def text(self):
        ''' Unformatted message body

            :getter: Get the unformatted message body
            :type: string
        '''
        return self._text

    @property
    def files(self):
        ''' URL of any files attached to message

            :getter: `list` of urls
            :type: list
        '''
        return [SparkFile(self._session, file) for file in self._files]

    @property
    def room(self):
        ''' `SparkRoom` object of parent room

            :getter: get parent spark room
            :type: `SparkRoom`
        '''

        return self._parent

    def __repr__(self):
        return f'SparkMessage({self.id})'
