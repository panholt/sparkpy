import os
from collections import deque
from time import sleep

import requests

from .models.room import SparkRoom
from .models.team import SparkTeam
from .models.container import SparkContainer
from .constants import SPARK_API_BASE, SPARK_PATHS


class SparkSession(requests.Session):

    def __init__(self, bearer_token=None):
        super().__init__()
        if not bearer_token:
            try:
                bearer_token = os.environ['SPARK_TOKEN']
            except KeyError:
                raise Exception('SparkSession Requires a bearer token')
        self.headers.update({'Authorization': 'Bearer ' + bearer_token,
                             'Content-type': 'application/json; charset=utf-8'})
        self.hooks = {'response': [self._retry_after_hook]}
        self._rooms = SparkContainer(self, SparkRoom)
        self._teams = SparkContainer(self, SparkTeam)

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

    def _make_generator(self, response, klass=None):
        data = response.json()
        d = deque(data.get('items', []))
        while d:
            if klass:
                yield klass(self, **d.popleft())
            else:
                yield d.popleft()
            if not d:
                if response.links.get('next'):
                    response = self.get(data.links['next']['url'])
                    d.extend(response.json()['items'])
                else:
                    return

    def __make_url(self, path):
        assert isinstance(path, str)
        root = path.lower().split('/')[0]
        if root in SPARK_PATHS:
            return SPARK_API_BASE + path
        return path

    @property
    def rooms(self):
        return self._rooms

    @property
    def teams(self):
        return self._teams

    def __repr__(self):
        return 'SparkSession()'
