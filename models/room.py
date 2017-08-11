from .message import SparkMessage
from .membership import SparkMembership
from .people import SparkPerson
from .container import SparkContainer
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt
from ..utils.uuid import is_api_id


class SparkRoom(object):

    API_BASE = f'{SPARK_API_BASE}rooms/'

    def __init__(self,  # *args, **kwargs):
                 spark,
                 id,
                 title,
                 type,
                 isLocked,
                 lastActivity,
                 created,
                 creatorId,
                 sipAddress=None,
                 teamId=None):

        self.spark = spark
        self._id = id
        self._title = title
        self._type = type
        self._isLocked = isLocked
        self._lastActivity = lastActivity
        self._created = created
        self._creatorId = creatorId
        self._sipAddress = sipAddress
        self._teamId = teamId
        self._path = 'rooms'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'
        self._messages = SparkContainer(self.spark,
                                        SparkMessage,
                                        params=self.message_params())
        self._members = SparkContainer(self.spark,
                                       SparkMembership,
                                       params={'roomId': self.id})

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        assert isinstance(value, str)
        assert len(value) > 0
        self.spark.put(self.path, json={'title': value})
        self._title = value
        return

    @property
    def type(self):
        return self._type

    @property
    def isLocked(self):
        return self._isLocked

    @property
    def lastActivity(self):
        return ts_to_dt(self._lastActivity)

    @property
    def created(self):
        return ts_to_dt(self._created)

    @property
    def creatorId(self):
        return self._creatorId

    @property
    def sipAddress(self):
        return self._sipAddress

    @property
    def teamId(self):
        return self._teamId

    @property
    def path(self):
        return self._path

    @property
    def messages(self):
        return self._messages

    def message_params(self):
        data = {'roomId': self.id}
        if self.spark.is_bot and self.type == 'group':
            data['mentionedPeople'] = 'me'
        return data

    def send_message(self, text):
        self.spark.send_message(text, room_id=self.id)
        return

    def delete(self):
        self.spark.delete(self.url)

    def add_person_by_id(self, person, moderator=False):
        if isinstance(person, SparkPerson):
            person = person.id
        elif not is_api_id(person):
            raise ValueError('Person must be a SparkPerson object or Spark API ID')
        self.spark.post('memberships', json={'roomId': self.id,
                                             'personId': person,
                                             'isModerator': moderator})
        return

    def add_person_by_email(self, email, moderator=False):
        assert '@' in email
        self.spark.post('memberships', json={'roomId': self.id,
                                             'personEmail': email,
                                             'isModerator': moderator})
        return

    def remove_person_by_id(self, person):
        if isinstance(person, SparkPerson):
            person = person.id
        elif not is_api_id(person):
            raise ValueError('Person must be a SparkPerson object or Spark API ID')
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

    def destroy(self):
        for member in self.members:
            if member.personId != self.spark.id:
                member.delete()
        self.delete()
        return

    def __repr__(self):
        return f'SparkRoom({self.id})'
