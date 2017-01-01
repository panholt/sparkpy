# -*- coding: utf-8 -*-

import os
import logging
from time import sleep

import requests

from .models.room import SparkRoom
from .models.team import SparkTeam
from .models.people import SparkPerson
from .models.container import SparkContainer
from .models.webhook import SparkWebhook
from .utils.uuid import is_api_id
from .constants import SPARK_API_BASE, SPARK_PATHS, \
                       WEBHOOK_FILTERS, WEBHOOK_EVENTS, WEBHOOK_RESOURCES

log = logging.getLogger('pyspark.session')


class SparkSession(requests.Session):

    def __init__(self, bearer_token=None):
        super().__init__()
        if not bearer_token:
            try:
                self._bearer_token = os.environ['SPARK_TOKEN']
            except KeyError:
                raise Exception('SparkSession Requires a bearer token')
        else:
            self._bearer_token = bearer_token
        self.headers.update({'Authorization': 'Bearer ' + self._bearer_token,
                             'Content-type': 'application/json; charset=utf-8'})
        self.hooks = {'response': [self._retry_after_hook]}
        self._id = None
        self._is_bot = None

    @property
    def rooms(self):
        return SparkContainer(self, SparkRoom)

    @property
    def teams(self):
        return SparkContainer(self, SparkTeam)

    @property
    def webhooks(self):
        return SparkContainer(self, SparkWebhook)

    @property
    def id(self):
        '''Returns the `personId` property of the bearer_token's owner
           :type: string '''
        if self._id is None:
            data = self.get('people/me').json()
            self._id = data['id']
            self._is_bot = data['type'] == 'bot'
        return self._id

    @property
    def is_bot(self):
        '''Returns `True` if bearer_token's owner is a bot
           type: bool '''
        if self._id is None:
            data = self.get('people/me').json()
            self._id = data['id']
            self._is_bot = data['type'] == 'bot'
        return self._is_bot

    def __make_url(self, path):
        assert isinstance(path, str)
        root = path.lower().split('/')[0]
        if root in SPARK_PATHS:
            return SPARK_API_BASE + path
        return path

    # Response session hooks
    def _retry_after_hook(self, response, *args, **kwargs):
        if response.status_code == 429:
            sleep_time = int(response.headers.get('Retry-After', 15))
            log.warning('Received a 429 Response. Backing off for %ss',
                        sleep_time)
            sleep(sleep_time)
            return self.send(response.request)

    # Override the requests base methods to automagically add the whole url.
    # eg: messages/{id} becomes https://api.ciscospark.com/v1/messages/{id}

    def get(self, path, **kwargs):
        url = self.__make_url(path)
        log.debug('Sending GET to %s', url)
        return super().get(url, **kwargs)

    def post(self, path, **kwargs):
        url = self.__make_url(path)
        log.debug('Sending POST to %s', url)
        return super().post(url, **kwargs)

    def put(self, path, **kwargs):
        url = self.__make_url(path)
        log.debug('Sending PUT to %s', url)
        return super().put(url, **kwargs)

    def delete(self, path, **kwargs):
        url = self.__make_url(path)
        log.debug('Sending DELETE to %s', url)
        return super().delete(url, **kwargs)

    def create_room(self, title, team_id=None):
        '''Create a Cisco Spark room

                :param title: Room title
                :type title: str

                :return: SparkTeam
            '''

        data = {'title': title}
        if team_id:
            assert is_api_id(team_id)
            data['teamId'] = team_id
        room = self.post('rooms', json=data).json()
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
        return SparkTeam(**team.json())

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
        webhook = self.post('webhooks', json=data)
        return SparkWebhook(**webhook.json())

    def send_message(self,
                     text,
                     room_id=None,
                     person_id=None,
                     person_email=None):
        '''Send a Cisco Spark message

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

        while len(text) > 7000:  # Technically 7439
            split_idx = text.rfind('\n', 1, 6999)
            if split_idx == -1:
                split_idx = 7000
            data = {'markdown': text[:split_idx]}
            data.update(base_data)
            self.post('messages', json=data)
            text = text[split_idx:]
        else:
            data = {'markdown': text}
            data.update(base_data)
            self.post('messages', json=data)
        return

    def __repr__(self):
        return 'SparkSession'
