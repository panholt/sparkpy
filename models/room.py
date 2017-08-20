from .base import SparkBase
from .time import SparkTime
from .membership import SparkMembership
from .container import SparkContainer
from ..session import SparkSession


class SparkRoom(SparkBase):

    API_BASE = 'https://api.ciscospark.com/v1/rooms/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='rooms', **kwargs)
        else:
            super().__init__(path='rooms', **kwargs)

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'title': {'type': str,
                          'optional': False,
                          'mutable': True},
                'type': {'type': str,
                         'optional': False,
                         'mutable': False},
                'isLocked': {'type': bool,
                             'optional': False,
                             'mutable': False},
                'lastActivity': {'type': SparkTime,
                                 'optional': False,
                                 'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False},
                'creatorId': {'type': str,
                              'optional': False,
                              'mutable': False},
                'sipAddress': {'type': str,
                               'optional': True,
                               'mutable': False},
                'teamId': {'type': str,
                           'optional': True,
                           'mutable': False}}

    def update(self, key, value):
        if key == 'title' and len(value):
            with SparkSession() as s:
                s.put(self.url, json={key: value})
        return

    @property
    def members(self):
        ''' Members of the Cisco Spark Room

            :getter: a generator like object of members of the room
            :type: `SparkContainer` of `SparkPeople` items
        '''
        return SparkContainer(SparkMembership,
                              params={'roomId': self.id},
                              parent=self)

    @property
    def message_params(self):
        ''' Retuns URL paramaters for /messages/

            Sets the `roomId` filter and if the session owner is a bot,
            the `mentionedPeople` filter is set to `me`

            :getter: url paramaters
            :type: dict
        '''
        data = {'roomId': self.id}
        if self.session.is_bot and self.type == 'group':
            data['mentionedPeople'] = 'me'
        return data

    def send_message(self, text, file=None):
        ''' Send a message to the room

            :param text: Markdown formatted text to send in message
            :type title: str

            :return: None
        '''
        with SparkSession() as s:
            s.send_message(text, room_id=self.id, file=file)
        return

    def add_member(self, *args, email='', moderator=False):
        ''' Add a person to the room

            :param email: email address of person to add
            :type email: str
            :param moderator: Default: False, Make person a moderator of room
            :type moderator: bool

            :return: None
        '''
        data = {'roomId': self.id}
        if args:
            # TODO Type checking
            data['personId'] = args[0]
        if '@' in email:
            data['personEmail'] = email
        if moderator:
            data['isModerator'] = moderator

        with SparkSession() as s:
            s.post('memberships', json=data)
        return

    def remove_member(self, *args, email=''):
        ''' Add a person to the room

            :param email: email address of person to add
            :type email: str
            :param moderator: Default: False, Make person a moderator of room
            :type moderator: bool

            :return: None
        '''

        if args:
            for member in self.members.filtered(lambda
                                                x: x.personId == args[0]):
                member.delete()
        elif '@' in email:
            for member in self.members.filtered(lambda
                                                x: x.personEmail == email):
                member.delete()
        return

    def remove_all_members(self):
        ''' Remove all people from the room leaving this account

            :return: None
        '''
        for member in self.members.filtered(lambda x: x != self.session.id):
            member.delete()
        return

    def __repr__(self):
        return f"SparkRoom('{self.id}')"
