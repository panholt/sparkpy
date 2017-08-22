from .utils import is_api_id
from .session import SparkSession
from .models.room import SparkRoom
from .models.people import SparkPerson
from .models.team import SparkTeam
from .models.webhook import SparkWebhook
from .models.container import SparkContainer


class Spark(object):

    def __init__(self):
        self._id = None
        self._is_bot = None

    @property
    def id(self):
        '''Returns the `personId` property of the bearer_token's owner
           :type: string '''
        if self._id is None:
            with SparkSession() as s:
                data = s.get('https://api.ciscospark.com/v1/people/me').json()
                self._id = data['id']
                self._is_bot = data['type'] == 'bot'
        return self._id

    @property
    def is_bot(self):
        '''Returns `True` if bearer_token's owner is a bot
           type: bool '''
        if self._is_bot is None:
            with SparkSession() as s:
                data = s.get('https://api.ciscospark.com/v1/people/me').json()
                self._id = data['id']
                self._is_bot = data['type'] == 'bot'
        return self._is_bot

    @property
    def rooms(self):
        return SparkContainer(SparkRoom, parent=self)

    @property
    def teams(self):
        return SparkContainer(SparkTeam, parent=self)

    @property
    def webhooks(self):
        return SparkContainer(SparkWebhook, parent=self)

    def create_room(self, title, team_id=None):
        '''Create a Cisco Spark room

                :param title: Room title
                :type title: str

                :return: SparkTeam
        '''

        data = {'title': title}
        if team_id:
            assert is_api_id(team_id, 'team')
            data['teamId'] = team_id
        with SparkSession() as s:
            room = s.post('rooms', json=data).json()
        return SparkRoom(**room)

    def create_one_on_one_room(self, person, message):
        '''Create or send a message to a 1:1 room

                :param person: Either a personId, email address, or API id
                :type person: str

                :return: SparkRoom
            '''

        isinstance(message, str) and len(message) > 0
        if isinstance(person, SparkPerson) or is_api_id(person):
            message = self.send_message(message, person_id=person.id)
        elif '@' in person:
            message = self.send_message(message, person_email=person)
        else:
            raise ValueError('Person must be an email address, SparkPerson, \
                             or Spark API ID')
        return message.room

    def create_team(self, name):
        '''Create a Cisco Spark webhook

                :param name: Team name
                :type name: str

                :return: SparkTeam
            '''

        team = self.post('teams', json={'name': name})
        return SparkTeam(self, **team.json())

    def create_webhook(self,
                       name,
                       target_url,
                       resource,
                       event,
                       filter=None,
                       secret=None):
        '''Create a Cisco Spark webhook

                :param name: Webhook name
                :type name: str

                :param target_url: Sets the `targetUrl` property
                :type target_url: str

                :param resource: Sets the `resource` property
                :type resource: str

                :param event: Sets the `event` property
                :type event: str

                :param person_id: Sets the `toPersonId` property
                :type person_id: str

                :param filter: Sets the `filter` property
                :type filter: str

                :param secret: Sets the `secret` property
                :type secret: str

                :return: SparkWebhook

                :raises: AssertionError
            '''

        WEBHOOK_RESOURCES = ['memberships', 'messages', 'rooms', 'all']
        WEBHOOK_EVENTS = ['created', 'updated', 'deleted', 'all']
        WEBHOOK_FILTERS = {'memberships': ['roomId',
                                           'personId',
                                           'personEmail',
                                           'isModerator'],
                           'messages': ['roomId',
                                        'roomType',
                                        'personId',
                                        'personEmail',
                                        'mentionedPeople',
                                        'hasFiles'],
                           'rooms': ['type',
                                     'isLocked']}
        assert resource in WEBHOOK_RESOURCES
        assert event in WEBHOOK_EVENTS
        data = {'name': name,
                'targetUrl': target_url,
                'resource': resource,
                'event': event}
        if filter:
            assert any([filter.starswith(item)
                        for item in WEBHOOK_FILTERS[resource]])
            data['filter'] = filter
        if secret:
            data['secret'] = secret
        with SparkSession() as s:
            webhook = s.post('webhooks', json=data)
            return SparkWebhook(**webhook.json())

    def send_message(self,
                     text,
                     room_id=None,
                     person_id=None,
                     person_email=None,
                     file=None):
        ''' Send a Cisco Spark message

            :param text: Markdown formatted message body
                         If message is longer than 7,000 characters
                         it is split at linebreak boundries
                         and sent as seperate messages
            :type text: str
            :param room_id: Sets the `roomId` property
            :type room_id: str
            :param person_id: Sets the `toPersonId` property
            :type person_id: str
            :param person_email: Sets the `toPersonEmailAddress` property
            :type person_id: str
            :param file: Path to file to upload
            :type file: str

            :return: None
            :raises ValueError: when none of 'room_id', 'person_id',
                                or 'person_email' are provided

            .. note:: This method must be called with exactly one of
                      'room_id', 'person_id', 'person_email'
        '''

        base_data = {}
        if room_id:
            assert is_api_id(room_id)
            base_data['roomId'] = room_id
        elif person_id:
            assert is_api_id(person_id)
            base_data['toPersonId'] = person_id
        elif person_email:
            assert '@' in person_email
            base_data['toPersonEmail'] = person_email
        else:
            raise ValueError('Must provide either a roomId, personId, \
                             or email address')

        with SparkSession() as s:
            while len(text) > 7000:  # Technically 7439
                split_idx = text.rfind('\n', 1, 6999)
                if split_idx == -1:
                    split_idx = 7000
                data = {'markdown': text[:split_idx]}
                data.update(base_data)
                if file:
                    s.send_file(file, data)
                    file = None
                else:
                    s.post('https://api.ciscospark.com/v1/messages', json=data)
                text = text[split_idx:]
            else:
                data = {'markdown': text}
                data.update(base_data)
                if file:
                    s.send_file(file, data)
                    return
                s.post('https://api.ciscospark.com/v1/messages', json=data)
            return

    def __repr__(self):
        return f'Spark("{self.id}")'
