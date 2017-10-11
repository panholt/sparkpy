from .base import SparkBase, SparkProperty
from .time import SparkTime
from .message import SparkMessage
from .membership import SparkMembership
from .container import SparkContainer


class SparkRoom(SparkBase):

    # | Start of class attributes |-------------------------------------------|
    API_BASE = 'https://api.ciscospark.com/v1/rooms/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'title': SparkProperty('title', mutable=True),
                  'type': SparkProperty('type'),
                  'isLocked': SparkProperty('islocked',
                                            optional=True),
                  'lastActivity': SparkProperty('lastActivity',
                                                optional=True),
                  'created': SparkProperty('created'),
                  'creatorId': SparkProperty('creatorId'),
                  'sipAddress': SparkProperty('sipAddress', optional=True),
                  'teamId': SparkProperty('teamId', optional=True)}

    # | Start of instance attributes |----------------------------------------|
    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='rooms', **kwargs)

    def update(self, key, value):
        if key == 'title' and len(value):
            self.parent.session.put(self.url, json={key: value})
        elif key == 'isLocked':
            raise NotImplemented('isLocked is not implemnted')
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
    def messages(self):
        ''' Messages in the Cisco Spark Room

            :getter: a generator like object of members of the room
            :type: `SparkContainer` of `SparkPeople` items
        '''
        return SparkContainer(SparkMessage,
                              params=self.message_params,
                              parent=self)

    @property
    def link(self):
        return f'https://web.ciscospark.com/rooms/{self.uuid}/chat'

    @property
    def message_params(self):
        ''' Retuns URL paramaters for /messages/

            Sets the `roomId` filter and if the session owner is a bot,
            the `mentionedPeople` filter is set to `me`

            :getter: url paramaters
            :type: dict
        '''
        data = {'roomId': self.id}
        if self.parent.is_bot and self.type == 'group':
            data['mentionedPeople'] = 'me'
        return data

    def send_message(self, text, file=None):
        ''' Send a message to the room

            :param text: Markdown formatted text to send in message
            :type title: str

            :return: None
        '''
        self.parent.send_message(text, room_id=self.id, file=file)
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
        self.parent.session.post(SparkMembership.API_BASE, json=data)
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
        for member in self.members.filtered(lambda x: x != self.parent.me.id):
            member.delete()
        return

    def __repr__(self):
        return f"SparkRoom('{self.id}')"
