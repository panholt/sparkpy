# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty
from .time import SparkTime
from .organization import SparkOrganization
from ..session import SparkSession


class SparkPerson(SparkBase):

    # | Start of class attributes |------------------------------------------ |
    API_BASE = 'https://api.ciscospark.com/v1/people/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'emails': SparkProperty('emails'),
                  'displayName': SparkProperty('displayName',
                                               mutable=True),
                  'avatar': SparkProperty('avatar',
                                          optional=True,
                                          mutable=True),
                  'orgId': SparkProperty('orgId'),
                  'created': SparkProperty('created'),
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
                                                optional=True),
                  'status': SparkProperty('status', optional=True),
                  'licenses': SparkProperty('licenses',
                                            optional=True,
                                            mutable=True),
                  'roles': SparkProperty('roles',
                                         optional=True),
                  'timezone': SparkProperty('timezone',
                                            optional=True),
                  'invitePending': SparkProperty('invitePending',
                                                 optional=True),
                  'loginEnabled': SparkProperty('loginEnabled',
                                                optional=True)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='people', **kwargs)
        self._org = None

    @property
    def email(self):
        # Emails is returned as an array but will
        # only ever have one entry.. or now anyway
        return self.emails[0]

    @property
    def org(self):
        if self._org is None:
            self._org = SparkOrganization(self.orgId)
        return self.org

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
