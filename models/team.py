# -*- coding: utf-8 -*-

from .base import SparkBase
from .time import SparkTime
from .membership import SparkTeamMembership
from .container import SparkContainer
from ..session import SparkSession


class SparkTeam(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/teams/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='teams', **kwargs)
        else:
            super().__init__(path='teams', **kwargs)

    def create_subroom(self, title):
        with SparkSession() as s:
            s.create_room(title, team_id=self.id)

    def update(self, key, value):
        if key == 'name' and len(value):
            with SparkSession() as s:
                s.put(self.url, json={key: value})
        return

    def add_member(self, *args, email='', moderator=False):
        ''' Add a person to the team

            :param email: email address of person to add
            :type email: str
            :param moderator: Default: False, Make person a moderator of room
            :type moderator: bool

            :return: None
        '''
        data = {'teamId': self.id}
        if args:
            # TODO Type checking
            data['personId'] = args[0]
        if '@' in email:
            data['personEmail'] = email
        if moderator:
            data['isModerator'] = moderator

        with SparkSession() as s:
            s.post('team/memberships', json=data)
        return

    def remove_member(self, *args, email=''):
        ''' Add a person to the team

            :param email: email address of person to add
            :type email: str
            :param moderator: Default: False, Make person a moderator of room
            :type moderator: bool

            :return: None
        '''

        if args:
            for member in self.members.filtered(lambda
                                                x: x.personId == args[0]):
                member.delete()
        elif '@' in email:
            for member in self.members.filtered(lambda
                                                x: x.personEmail == email):
                member.delete()
        return

    def remove_all_members(self):
        ''' Remove all people from the room leaving this account

            :return: None
        '''
        for member in self.members.filtered(lambda x: x != self.session.id):
            member.delete()
        return

    @property
    def link(self):
        return f'https://web.ciscospark.com/teams/{self.id}'

    @property
    def members(self):
        '''SparkContainer:`SparkTeamMembership`
           Generator of members of the team.'''

        return SparkContainer(SparkTeamMembership,
                              params={'teamId': self.id})

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'name': {'type': str,
                         'optional': False,
                         'mutable': True},
                'creatorId': {'type': str,
                              'optional': False,
                              'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False}}
