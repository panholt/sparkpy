# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty
from .time import SparkTime
from ..session import SparkSession


class SparkMembership(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/memberships/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'roomId': SparkProperty('roomId'),
                  'personId': SparkProperty('personId'),
                  'personEmail': SparkProperty('personEmail'),
                  'personOrgId': SparkProperty('personOrgId'),
                  'personDisplayName': SparkProperty('personDisplayName'),
                  'isModerator': SparkProperty('isModerator',
                                               mutable=True,
                                               optional=True),
                  'isMonitor': SparkProperty('isMonitor', optional=True),
                  'created': SparkProperty('created', cls=SparkTime)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='memberships', **kwargs)

    def update(self, key, value):
        if key == 'isModerator':
            with SparkSession() as s:
                s.put(self.url, json={key: value})
        return


class SparkTeamMembership(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/team/memberships/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'teamId': SparkProperty('teamId'),
                  'personId': SparkProperty('personId'),
                  'personEmail': SparkProperty('personEmail'),
                  'personOrgId': SparkProperty('personOrgId'),
                  'personDisplayName': SparkProperty('personDisplayName'),
                  'isModerator': SparkProperty('isModerator',
                                               mutable=True,
                                               optional=True),
                  'created': SparkProperty('created', cls=SparkTime)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='team/memberships', **kwargs)

    def update(self, key, value):
        if key == 'isModerator':
            with SparkSession() as s:
                s.put(self.url, json={key: value})
        return

    def __repr__(self):
        return f'SparkTeamMembership({self.id})'
