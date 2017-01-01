from .message import SparkMessage
from .membership import SparkMembership
from .people import SparkPerson
from .container import SparkContainer
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt
from ..utils.uuid import is_api_id
from .base import SparkBase


class SparkRoom(SparkBase):

    ''' Cisco Spark Room Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param parent: The parent spark team if present
        :param \**kwargs: All standard Spark API properties for a Room
    '''

    API_BASE = f'{SPARK_API_BASE}rooms/'

    def __init__(self,
                 session,
                 id,
                 title,
                 type,
                 isLocked,
                 lastActivity,
                 created,
                 creatorId,
                 sipAddress=None,
                 teamId=None,
                 parent=None):

        super().__init__(session, id, 'rooms', parent=parent)
        self.session = session
        self._title = title
        self._type = type
        self._isLocked = isLocked
        self._lastActivity = lastActivity
        self._created = created
        self._creatorId = creatorId
        self._sipAddress = sipAddress
        self._teamId = teamId

    @property
    def title(self):
        ''' Room title

            :getter: Gets the room title
            :setter: Sets the room title
            :type: string
        '''
        return self._title

    @title.setter
    def title(self, value):
        assert isinstance(value, str)
        assert len(value) > 0
        self.session.put(self.path, json={'title': value})
        self._title = value
        return

    @property
    def type(self):
        ''' Room type

            Can be either 'direct' or 'group'

            :getter: Gets the room type
            :type: string
        '''
        return self._type

    @property
    def isLocked(self):
        ''' Is room locked

            :getter: returns `True` if room is locked
            :type: bool
        '''
        return self._isLocked

    @property
    def lastActivity(self):
        ''' Last activity time

            :getter: returns datetime object of last activity time
            :type: datetime.datetime
        '''
        return ts_to_dt(self._lastActivity)

    @property
    def created(self):
        ''' Room created time

            :getter: returns datetime object of room creation time
            :type: datetime.datetime
        '''
        return ts_to_dt(self._created)

    @property
    def creatorId(self):
        ''' Creater id of room

            :getter: the API id of the creater of the room
            :type: str
        '''
        return self._creatorId

    @property
    def sipAddress(self):
        ''' The SIP address of the room

            :getter: the SIP address of the room if present
            :type: str
        '''
        return self._sipAddress

    @property
    def teamId(self):
        ''' Team id of the room if room is part of a team

            :getter: `teamId` property
            :type: str
        '''
        return self._teamId

    @property
    def messages(self):
        return SparkContainer(self.session, SparkMessage,
                              params=self._message_params(),
                              parent=self)

    @property
    def members(self):
        return SparkContainer(self.session, SparkMembership,
                              params={'roomId': self.id},
                              parent=self)

    def _message_params(self):
        data = {'roomId': self.id}
        if self.session.is_bot and self.type == 'group':
            data['mentionedPeople'] = 'me'
        return data

    def send_message(self, text):
        ''' Send a message to the room

            :param text: Markdown formatted text to send in message
            :type title: str

            :return: None
        '''
        print(f'Sending {text} to {self.id}')
        self.session.send_message(text, room_id=self.id)
        return

    def add_person_by_id(self, person, moderator=False):
        ''' Add a person to the room by id

            :param person: personId or  `SparkPerson` to add to room
            :type person: str or `SparkPerson` object
            :param moderator: Default: False, Make person a moderator of room
            :type moderator: bool

            :return: None
        '''
        if isinstance(person, SparkPerson):
            person = person.id
        elif not is_api_id(person):
            raise ValueError('Person must be a SparkPerson object \
                              or Spark API ID')
        self.session.post('memberships', json={'roomId': self.id,
                                               'personId': person,
                                               'isModerator': moderator})
        return

    def add_person_by_email(self, email, moderator=False):
        ''' Add a person to the room by email address

            :param email: email address of person to add
            :type email: str
            :param moderator: Default: False, Make person a moderator of room
            :type moderator: bool

            :return: None
        '''
        assert '@' in email
        self.session.post('memberships', json={'roomId': self.id,
                                               'personEmail': email,
                                               'isModerator': moderator})
        return

    def remove_person_by_id(self, person):
        ''' Remove a person to the room by id

            :param person: personId or  `SparkPerson` to add to room
            :type person: str or `SparkPerson` object

            :return: None
        '''
        if not isinstance(person, SparkPerson) or not is_api_id(person):
            raise ValueError('Person must be a SparkPerson object or \
                             Spark API ID')
        for member in self.members.filtered(lambda x: x == person):
            member.delete()
        return

    def remove_person_by_email(self, email):
        ''' Remove a person to the room by email address

            :param email: email address of person to add

            :return: None
        '''
        if '@' not in email:
            raise ValueError('Must provide valid email address')
        for member in self.members.filtered(lambda x: x.personEmail == email):
            member.delete()
        return

    def remove_all_people(self):
        ''' Remove all people from the room leaving this account

            :return: None
        '''
        for member in self.members.filtered(lambda x: x != self.session.id):
            member.delete()
        self.delete()
        return

    def __repr__(self):
        return f'SparkRoom({self.id})'
