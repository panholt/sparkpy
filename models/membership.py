# -*- coding: utf-8 -*-

from .base import SparkBase
from .time import SparkTime
from ..session import SparkSession


class SparkMembership(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/memberships/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='memberships', **kwargs)
        else:
            super().__init__(path='memberships', **kwargs)

    def update(self, key, value):
        if key == 'isModerator':
            with SparkSession() as s:
                s.put(self.url, json={key: value})
        return

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'roomId': {'type': str,
                           'optional': False,
                           'mutable': False},
                'personId': {'type': str,
                             'optional': False,
                             'mutable': False},
                'personEmail': {'type': str,
                                'optional': False,
                                'mutable': False},
                'personOrgId': {'type': str,
                                'optional': False,
                                'mutable': False},
                'personDisplayName': {'type': str,
                                      'optional': False,
                                      'mutable': False},
                'isModerator': {'type': bool,
                                'optional': False,
                                'mutable': False},
                'isMonitor': {'type': bool,
                              'optional': False,
                              'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False}}


class SparkTeamMembership(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/team/memberships/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='team/memberships', **kwargs)
        else:
            super().__init__(path='team/memberships', **kwargs)

    def update(self, key, value):
        if key == 'isModerator':
            with SparkSession() as s:
                s.put(self.url, json={key: value})
        return

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'teamId': {'type': str,
                           'optional': False,
                           'mutable': False},
                'personId': {'type': str,
                             'optional': False,
                             'mutable': False},
                'personEmail': {'type': str,
                                'optional': False,
                                'mutable': False},
                'personOrgId': {'type': str,
                                'optional': False,
                                'mutable': False},
                'personDisplayName': {'type': str,
                                      'optional': False,
                                      'mutable': False},
                'isModerator': {'type': bool,
                                'optional': False,
                                'mutable': False},
                'isMonitor': {'type': bool,
                              'optional': False,
                              'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False}}

    def __repr__(self):
        return f'SparkTeamMembership({self.id})'
