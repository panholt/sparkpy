# -*- coding: utf-8 -*-

from .base import SparkBase  # , SparkProperty
from .time import SparkTime


class SparkWebhook(SparkBase):

    ''' Cisco Spark Webhook Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param \**kwargs: All standard Spark API properties for a Webhook
    '''

    # Class level constants
    @property
    def API_BASE(self):
        return 'https://api.ciscospark.com/v1/webhooks/'

    @property
    def WEBHOOK_RESOURCES(self):
        return ['memberships', 'messages', 'rooms', 'all']

    @property
    def WEBHOOK_EVENTS(self):
        return ['created', 'updated', 'deleted', 'all']

    @property
    def WEBHOOK_FILTERS(self):
        return {'memberships': ['roomId',
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

    # id = SparkProperty('id')
    # name = SparkProperty('name')
    # targetUrl = SparkProperty('targetUrl')
    # event = SparkProperty('event')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='webhooks', **kwargs)

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
