# -*- coding: utf-8 -*-

import os
import logging
import mimetypes
from time import sleep

import requests
from requests_toolbelt import MultipartEncoder

from .constants import SPARK_API_BASE, SPARK_PATHS

log = logging.getLogger('sparkpy.session')


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
    def id(self):
        '''Returns the `personId` property of the bearer_token's owner
           :type: string '''
        if self._id is None:
            data = self.get('https://api.ciscospark.com/v1/people/me').json()
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

    def __send_file(self, file, data):
        filetype = mimetypes.guess_type(file)[0]
        fname = os.path.abspath(file).rsplit(os.sep)[-1]
        data.update({'files': (fname, open(file, 'rb'), filetype)})
        multipart = MultipartEncoder(fields=data)
        self.post('messages',
                  headers={'Content-type': multipart.content_type},
                  data=multipart)
        return

    # Response session hooks
    def _retry_after_hook(self, response, *args, **kwargs):
        if response.status_code == 429:
            sleep_time = int(response.headers.get('Retry-After', 15))
            log.warning('Received a 429 Response. Backing off for %ss',
                        sleep_time)
            sleep(sleep_time)
            return self.send(response.request)

    def __repr__(self):
        return 'SparkSession'
