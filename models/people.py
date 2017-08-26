# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty
from .time import SparkTime
from ..session import SparkSession


class SparkPerson(SparkBase):

    # | Start of class attributes |------------------------------------------ |
    api_base = 'https://api.ciscospark.com/v1/people/'
    properties = {'id': SparkProperty('id'),
                  'emails': SparkProperty('emails'),
                  'displayName': SparkProperty('displayName',
                                               mutable=True),
                  'avatar': SparkProperty('avatar',
                                          optional=True,
                                          mutable=True),
                  'orgId': SparkProperty('orgId'),
                  'created': SparkProperty('created',
                                           cls=SparkTime),
                  'type': SparkProperty('type'),
                  'firstName': SparkProperty('firstName',
                                             optional=True,
                                             mutable=True),
                  'lastName': SparkProperty('lastName',
                                            optional=True,
                                            mutable=True),
                  'nickName': SparkProperty('nickName',
                                            optional=True,
                                            mutable=True),
                  'lastActivity': SparkProperty('lastActivity',
                                                optional=True,
                                                cls=SparkTime),
                  'status': SparkProperty('status', optional=True),
                  'licenses': SparkProperty('licenses',
                                            optional=True,
                                            mutable=True),
                  'roles': SparkProperty('roles',
                                         optional=True),
                  'timezone': SparkProperty('timezone',
                                            optional=True),
                  'invitePending': SparkProperty('invitePending',
                                                 optional=True,
                                                 cls=bool),
                  'loginEnabled': SparkProperty('loginEnabled',
                                                optional=True,
                                                cls=bool)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='people', **kwargs)

        # Start of instance attributes |--------------------------------------|
        self._email = None

    @property
    def email(self):
        # Emails is returned as an array but will
        # only ever have one entry.. or now anyway
        if not self._email:
            self._email = self.emails[0]
        return self._email

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

    def __repr__(self):
        return f"SparkPerson('{self.id}')"

    def __str__(self):
        return f"SparkPerson('{self.displayName}')"
