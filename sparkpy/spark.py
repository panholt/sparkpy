'''
sparkpy Module
~~~~~~~~~~~~~~
sparkpy is a library written in Python3 for Cisco Spark that uses native
python methods to interact with the Cisco Spark API in a pythonic way.

Usage example:
    >>> from sparkpy import Spark
    >>> spark = Spark()  # Use the SPARK_TOKEN environment varible
    >>> # Alternatively spark = Spark('MY TOKEN')
    >>> for room in spark.rooms:
        ... print(f'{room.title}')
    >>> room = spark.create_room('Sample Room')
    >>> room.add_member('panholt@gmail.com')
    >>> # Rename the room title
    >>> room.title = 'A different title'
    >>> # Delete the room
    >>> room.delete()

There are many more features added please consult the documentation at
{documentation placeholder}

:copyright: (c) 2017 by Paul Anholt
:license: MIT, see LICENSE for more details.
'''


from os import environ
from .utils import is_api_id
from .session import SparkSession
from .models.room import SparkRoom
from .models.team import SparkTeam
from .models.people import SparkPerson
from .models.webhook import SparkWebhook
from .models.container import SparkContainer
from json.decoder import JSONDecodeError

class Spark(object):
    '''
    A :class:`Spark <Spark>` object.
    Used as the main interaction between the sparkpy module and Cisco Spark API

    :param token: (optional) The bearer token for the Cisco Spark API
                  If this paramater is not provided then the token is
                  taken from the `SPARK_TOKEN` environment variable
    Usage:
      >>> from sparkpy import Spark
      >>> spark = Spark()
    '''

    def __init__(self, token=None):
        self._id = None
        self._me = None
        self._is_bot = None
        if token:
            self._session = SparkSession(token)
        else:
            try:
                self._session = SparkSession(environ['SPARK_TOKEN'])
            except KeyError as e:
                # TODO exceptions
                raise Exception('Please insert token')

    @property
    def id(self):
        '''
        Returns the `personId` property of the bearer_token's owner

        :type: string
        '''
        if self._id is None:
            self._fetch_self()
        return self._id

    @property
    def session(self):
        '''
        A :class:`SparkSession <SparkSession>` object.
        A subclassed requests session, bound to a single :class:`Spark <Spark>`
        instance so `429` Responses are handled properly
        '''
        return self._session

    @property
    def me(self):
        ''' :class:`SparkPerson <SparkPerson>` of the token's owner '''
        if self._me is None:
            self._fetch_self()
        return self._me

    @property
    def is_bot(self):
        '''
        Returns `True` if bearer_token's owner is a bot
        type: bool
        '''
        if self._is_bot is None:
            self._fetch_self()
        return self._is_bot

    @property
    def rooms(self):
        '''
        A :class:`SparkContainer <SparkContainer>` object.
        Returns a generator like object yielding :class:`Sparkroom <Sparkroom>`
        objects.
        Also provides dict style lookups using a `roomId`, list style indexing,
        and slicing.
        '''
        return SparkContainer(SparkRoom, parent=self)

    @property
    def teams(self):
        '''
        A :class:`SparkContainer <SparkContainer>` object.
        Returns a generator like object yielding :class:`SparkTeam <SparkTeam>`
        objects.
        Also provides dict style lookups using a `teamId`, list style indexing,
        and slicing.
        '''
        return SparkContainer(SparkTeam, parent=self)

    @property
    def webhooks(self):
        '''
        A :class:`SparkContainer <SparkContainer>` object.
        Returns a generator like object yielding
        :class:`SparkWebhook <SparkWebhook>` objects.
        Also provides dict style lookups using a `roomId`, list style indexing,
        and slicing.
        '''
        return SparkContainer(SparkWebhook, parent=self)

    def search_people(self, query, org_id=None, max_=None):
        '''
        Query the Cisco Spark API for people.

        :param query: The query string, may be a Cisco Spark API id,
                      an email address, or a list of Cisco Spark API id's
        :param org_id: (optional) A Cisco Spark Organization id
        :param max_: (optional) `int` limit the results to `max` numbers
        '''
        params = {}
        if is_api_id(query, 'people'):
            params.update({'id'})
        elif '@' in query:
            params.update({'email': query})
        elif isinstance(query, list):
            params.update({'id': ','.join(query)})
        else:
            params.update({'displayName': query})
        if org_id:
            params.update({'orgId': org_id})
        if max_ and isinstance(max_, int):
            params.update({'max': max_})
        return SparkContainer(SparkPerson, parent=self, params=params)

    def _fetch_self(self):
        '''
        Internal method used to get the details of the token owner, and
        validate the bearer token

        :raises: `Exception`
        '''
        resp = self.session.get('https://api.ciscospark.com/v1/people/me')
        if resp.status_code == 200:
            try:
                data = resp.json()
            except JSONDecodeError:
                # TODO exceptions
                raise Exception('Failed to retrieve self details')

            self._id = data['id']
            self._me = SparkPerson(parent=self, **data)
            self._is_bot = self.me.type == 'bot'
        else:
            # TODO exceptions
            raise Exception(f'Invalid status code {r.status_code}: {r.text}')

    def create_room(self, title, team_id=None):
        '''
        Create a Cisco Spark room

                :param title: Room title
                :type title: str
                :param team_id: A Cisco Spark Team API id if room is to be a
                                subroom of a :class:`SparkTeam <SparkTeam>`
                :type team_id: str

                :return: :class:`SparkRoom <SparkRoom>`
        '''

        data = {'title': title}
        if team_id:
            assert is_api_id(team_id, 'team')
            data['teamId'] = team_id

        room = self.session.post('https://api.ciscospark.com/v1/rooms',
                                 json=data).json()
        return SparkRoom(parent=self, **room)

    def create_one_on_one_room(self, person, message):
        '''
        Create or send a message to a 1:1 room

        :param person: Either a personId, email address,
                       or Cisco Spark person API id
        :type person: str
        :param message: The markdown formatted message to send
        :type person: str

        :return: :class:`SparkRoom <SparkRoom>`
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
        assert resource in SparkWebhook.WEBHOOK_RESOURCES
        assert event in SparkWebhook.WEBHOOK_EVENTS
        data = {'name': name,
                'targetUrl': target_url,
                'resource': resource,
                'event': event}
        if filter:
            assert any([filter.starswith(item)
                        for item in SparkWebhook.WEBHOOK_FILTERS[resource]])
            data['filter'] = filter
        if secret:
            data['secret'] = secret
        hook = self.session.post('https://api.ciscospark.com/v1/webhooks',
                                 json=data)
        return SparkWebhook(**hook.json())

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
                      `room_id`, `person_id`, or `person_email`
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

        # Chunk and send the message
        while len(text) > 7000:  # Technically 7439
            split_idx = text.rfind('\n', 1, 6999)
            if split_idx == -1:
                split_idx = 7000
            data = {'markdown': text[:split_idx]}
            data.update(base_data)
            # Send any files waiting
            if file:
                self.session.send_file(file, data)
                # TODO make this a list or something
                file = None
            else:
                self.session.post('https://api.ciscospark.com/v1/messages',
                                  json=data)
            text = text[split_idx:]
        else:
            data = {'markdown': text}
            data.update(base_data)
            if file:
                self.session.send_file(file, data)
                return
            self.session.post('https://api.ciscospark.com/v1/messages',
                              json=data)
            return

    def __repr__(self):
        return f'Spark("{self.id}")'
