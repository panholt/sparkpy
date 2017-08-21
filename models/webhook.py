# -*- coding: utf-8 -*-

from .base import SparkBase
from .time import SparkTime


class SparkWebhook(SparkBase):

    ''' Cisco Spark Webhook Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param \**kwargs: All standard Spark API properties for a Webhook
    '''

    API_BASE = 'https://api.ciscospark.com/v1/webhooks/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='webhooks', **kwargs)
        else:
            super().__init__(path='webhooks', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'name': {'type': str,
                         'optional': False,
                         'mutable': False},
                'targetUrl': {'type': str,
                              'optional': False,
                              'mutable': False},
                'event': {'type': str,
                          'optional': False,
                          'mutable': False},
                'orgId': {'type': str,
                          'optional': False,
                          'mutable': False},
                'createdBy': {'type': str,
                              'optional': False,
                              'mutable': False},
                'appId': {'type': str,
                          'optional': False,
                          'mutable': False},
                'ownedBy': {'type': str,
                            'optional': False,
                            'mutable': False},
                'status': {'type': str,
                           'optional': False,
                           'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False},
                'filter': {'type': str,
                           'optional': True,
                           'mutable': False},
                'secret': {'type': str,
                           'optional': True,
                           'mutable': False}}

    def __repr__(self):
            return f'SparkLicense("{self.id}")'

    def __str__(self):
            return f'SparkLicense({self.name})'
