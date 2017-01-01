from .base import SparkBase
from .container import SparkContainer
from .room import SparkRoom
from .people import SparkPerson
from .membership import SparkTeamMembership
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt
from ..utils.uuid import is_api_id

class SparkTeam(SparkBase):

    ''' SparkTeam object reprsents a Team in Cisco Spark

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    '''

    API_BASE = f'{SPARK_API_BASE}teams/'

    def __init__(self, spark, id, name, created, creatorId):
        super().__init__(id, 'teams')
        self.spark = spark
        self._name = name
        self._created = created
        self._creatorId = creatorId

    @property
    def name(self):
        '''str: The name of the Cisco Spark Team.
                 Setter will invoke the API 
        '''
        return self._name

    @name.setter
    def name(self, val):
        self.spark.put(self.url, json={'name': val})
        self._val = val
        return

    @property
    def created(self):
        '''datetime.datetime: A datetime object representing 
           the time that the team was created
        '''
        return ts_to_dt(self._created)

    @property
    def creatorId(self):
        '''str: The ID of the creator of the room'''
        return self._creatorId

    @property
    def subrooms(self):
        '''SparkContainer:`SparkRoom`
           Generator of subrooms belonging to the team.'''

        return SparkContainer(self.spark, SparkRoom,
                              params={'teamId': self.id,
                                      'sortBy': 'id'})

    @property
    def members(self):
        '''SparkContainer:`SparkTeamMembership`
           Generator of members of the team.'''

        return SparkContainer(self.spark, SparkTeamMembership,
                              params={'teamId': self.id})

    def delete(self):
        self.spark.delete(self.url)

    def create_subroom(self, title):
        return self.spark.create_room(title, team_id=self.id)

    def add_person_by_id(self, person, moderator=False):
        if isinstance(person, SparkPerson):
            person = person.id
        elif not is_api_id(person):
            raise ValueError('Person must be a SparkPerson object \
                              or Spark API ID')
        self.spark.post('team/memberships', json={'teamId': self.id,
                                                  'personId': person,
                                                  'isModerator': moderator})
        return

    def add_person_by_email(self, email, moderator=False):
        assert '@' in email
        self.spark.post('team/memberships', json={'teamId': self.id,
                                                  'personEmail': email,
                                                  'isModerator': moderator})
        return

    def remove_person_by_id(self, person):
        if isinstance(person, SparkPerson):
            person = person.id
        elif not is_api_id(person):
            raise ValueError('Person must be a SparkPerson object or \
                             Spark API ID')
        for member in self.members:
            if member.id == person:
                member.delete()
        return

    def remove_person_by_email(self, email, moderator=False):
        assert '@' in email
        for member in self.members:
            if member.personEmail == email:
                member.delete()
        return

    def __repr__(self):
        return f'SparkTeam({self.id})'
