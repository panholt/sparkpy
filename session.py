import os
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


class SparkSession(requests.Session):

    def __init__(self, bearer_token=None):
        super().__init__()
        if not bearer_token:
            try:
                self._bearer_token = os.environ['SPARK_TOKEN']
            except KeyError:
                raise Exception('SparkSession Requires a bearer token')
        self.headers.update({'Authorization': 'Bearer ' + self.bearer_token,
                             'Content-type': 'application/json; charset=utf-8'})
        self.hooks = {'response': [self._retry_after_hook]}
        self._rooms = SparkContainer(self, SparkRoom)
        self._teams = SparkContainer(self, SparkTeam)
        self._webhooks = SparkContainer(self, SparkWebhook)
        self._id, self._is_bot = self.__get_self()

    @property
    def rooms(self):
        return self._rooms

    @property
    def teams(self):
        return self._teams

    @property
    def webhooks(self):
        return self._webhooks

    @property
    def bearer_token(self):
        return self._bearer_token

    @property
    def id(self):
        return self._id

    @property
    def is_bot(self):
        return self._is_bot

    def __make_url(self, path):
        assert isinstance(path, str)
        root = path.lower().split('/')[0]
        if root in SPARK_PATHS:
            return SPARK_API_BASE + path
        return path

    def __get_self(self):
        data = self.get('people/me').json()
        return data['id'], data['type'] == 'bot'

    # Response session hooks
    def _retry_after_hook(self, response, *args, **kwargs):
        if response.status_code == 429:
            sleep_time = int(response.headers.get('Retry-After', 15))
            sleep(sleep_time)
            return self.send(response.request)

    # Override the requests base methods to automagically add the whole url.
    # eg: messages/{id} becomes https://api.ciscospark.com/v1/messages/{id}

    def get(self, path, **kwargs):
        return super().get(self.__make_url(path), **kwargs)

    def post(self, path, **kwargs):
        return super().post(self.__make_url(path), **kwargs)

    def put(self, path, **kwargs):
        return super().put(self.__make_url(path), **kwargs)

    def delete(self, path, **kwargs):
        return super().delete(self.__make_url(path), **kwargs)

    def create_room(self, title, team_id=None):
        data = {'title': title}
        if team_id:
            assert is_api_id(team_id)
            data['teamId'] = team_id
        room = self.post('rooms', json=data).json()
        return self.rooms[room['id']]

    def create_one_on_one_room(self, person, message):
        assert isinstance(message, str) and len(message) > 0
        data = {'markdown': message}
        if isinstance(person, SparkPerson):
            data['toPersonId'] = person.id
        elif '@' in person:
            data['toPersonEmail'] = person
        elif is_api_id(person):
            data['toPersonId'] = person
        else:
            raise ValueError('Person must be an email address, SparkPerson, \
                             or Spark API ID')

        _message = self.post('messages', json=data).json()
        return self.rooms[_message['roomId']]

    def create_team(self, name):
        team = self.post('teams', json={'name': name}).json()
        return self.teams[team['id']]

    def create_webhook(self,
                       name,
                       target_url,
                       resource,
                       event,
                       filter=None,
                       secret=None):

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
        webhook = self.post('webhooks', json=data).json()
        return self.webhooks[webhook['id']]

    def send_message(self,
                     text,
                     room_id=None,
                     person_id=None,
                     person_email=None):
        ''' Method to chunk and send messages'''
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
        return 'SparkSession()'
