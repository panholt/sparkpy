# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty
from .time import SparkTime


class SparkWebhook(SparkBase):

    ''' Cisco Spark Webhook Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param \**kwargs: All standard Spark API properties for a Webhook
    '''

    # | Start of class attributes |-------------------------------------------|

    API_BASE = 'https://api.ciscospark.com/v1/webhooks/'
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
    PROPERTIES = {'id': SparkProperty('id'),
                  'name': SparkProperty('name', mutable=True),
                  'targetUrl': SparkProperty('targetUrl', mutable=True),
                  'event': SparkProperty('event'),
                  'resource': SparkProperty('resource'),
                  'filter': SparkProperty('filter', optional=True),
                  'secret': SparkProperty('secret', optional=True),
                  'orgId': SparkProperty('orgId', optional=True),
                  'createdBy': SparkProperty('createdBy', optional=True),
                  'appId': SparkProperty('appId', optional=True),
                  'ownedBy': SparkProperty('ownedBy', optional=True),
                  'status': SparkProperty('status', optional=True),
                  'created': SparkProperty('created', optional=True)}

    # | Start of instance attributes |----------------------------------------|
    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='webhooks', **kwargs)

    def update(self, name, targetUrl):
        data = {'name': name, 'targetUrl': targetUrl}
        self.parent.session.put(self.API_BASE, json=data)
        return

    def __repr__(self):
            return f'SparkWebhook("{self.id}")'

    def __str__(self):
            return f'SparkWebhook({self.name})'
