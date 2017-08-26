# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty
from .time import SparkTime
from .membership import SparkTeamMembership
from .container import SparkContainer
from .room import SparkRoom
from ..session import SparkSession


class SparkTeam(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    api_base = 'https://api.ciscospark.com/v1/teams/'

    properties = {'id': SparkProperty('id'),
                  'name': SparkProperty('name', mutable=True),
                  'creatorId': SparkProperty('creatorId'),
                  'created': SparkProperty('created', cls=SparkTime)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='teams', **kwargs)
        self._parent = kwargs.get('parent')

    @property
    def parent(self):
        return self._parent

    def update(self, key, value):
        if key == 'name' and len(value):
            with SparkSession() as s:
                s.put(self.url, json={key: value})
        return

    def create_subroom(self, title):
        with SparkSession() as s:
            s.create_room(title, team_id=self.id)

    def add_member(self, _id, email='', moderator=False):
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
            data['personId'] = _id
        if '@' in email:
            data['personEmail'] = email
        if moderator:
            data['isModerator'] = moderator

        with SparkSession() as s:
            s.post('team/memberships', json=data)
        return

    def remove_member(self, _id, email=''):
        ''' Add a person to the team

            :param email: email address of person to add
            :type email: str
            :param moderator: Default: False, Make person a moderator of room
            :type moderator: bool

            :return: None
        '''

        if args:
            for member in self.members.filtered(lambda
                                                x: x.personId == _id):
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
                              params={'teamId': self.id},
                              parent=self)

    @property
    def subrooms(self):
        '''SparkContainer:`SparkRoom`
           Generator of members of the team.'''

        return SparkContainer(SparkRoom,
                              params={'teamId': self.id,
                                      'sortBy': 'id'},
                              parent=self)

    def __str__(self):
        return f'SparkTeam("{self.name}")'

    def __repr__(self):
        return f'SparkTeam("{self.id}")'

