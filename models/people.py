# -*- coding: utf-8 -*-

from .base import SparkBase
from .time import SparkTime
from ..session import SparkSession


class SparkPerson(SparkBase):

    API_BASE = 'https://api.ciscospark.com/v1/people/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='people', **kwargs)
        else:
            super().__init__(path='people', **kwargs)
        self._email = None

    @property
    def email(self):
        # Emails is returned as an array but will only ever have one entry
        # For now anyway
        if not self._email:
            self._email = self.emails[0]
        return self._email

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'emails': {'type': list,
                           'optional': False,
                           'mutable': False},
                'displayName': {'type': str,
                                'optional': False,
                                'mutable': True},
                'avatar': {'type': str,
                           'optional': True,
                           'mutable': True},
                'orgId': {'type': str,
                          'optional': False,
                          'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False},
                'type': {'type': str,
                         'optional': False,
                         'mutable': False},
                'firstName': {'type': str,
                              'optional': True,
                              'mutable': True},
                'lastName': {'type': str,
                             'optional': True,
                             'mutable': True},
                'nickName': {'type': str,
                             'optional': True,
                             'mutable': True},
                'lastActivity': {'type': SparkTime,
                                 'optional': True,
                                 'mutable': False},
                'status': {'type': str,
                           'optional': True,
                           'mutable': False},
                'licenses': {'type': str,
                             'optional': True,
                             'mutable': True},
                'roles': {'type': str,
                          'optional': True,
                          'mutable': False},
                'timezone': {'type': str,
                             'optional': True,
                             'mutable': False},
                'invitePending': {'type': bool,
                                  'optional': True,
                                  'mutable': False},
                'loginEnabled': {'type': bool,
                                 'optional': True,
                                 'mutable': False}}

    def update(self,
               emails=None,
               displayName=None,
               firstName=None,
               lastName=None,
               avatar=None,
               orgId=None,
               roles=None,
               licenses=None):

        updates = {k: v for k, v in locals().items() if k != 'self' and v}
        with SparkSession() as s:
            existing_data = s.get(self.url).json()
            existing_data.update(updates)
            s.put(self.url, json=existing_data)
        return

    # def __repr__(self):
    #     return f"SparkPerson('{self.id}')"

    # def __str__(self):
    #     return f"SparkPerson('{self.displayName}')"
