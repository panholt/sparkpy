from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt
from .base import SparkBase


class SparkMembership(SparkBase):

    ''' Cisco Spark Membership Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param parent: The parent spark room
        :param \**kwargs: All standard Spark API properties for a Membership
    '''
    API_BASE = f'{SPARK_API_BASE}memberships/'

    def __init__(self,
                 session,
                 id,
                 roomId,
                 personId,
                 personEmail,
                 personDisplayName,
                 personOrgId,
                 isModerator,
                 isMonitor,
                 created,
                 parent=None):

        super().__init__(session, id, 'memberships', parent=parent)
        self._roomId = roomId
        self._personId = personId
        self._personEmail = personEmail
        self._personDisplayName = personDisplayName
        self._personOrgId = personOrgId
        self._isModerator = isModerator
        self._isMonitor = isMonitor
        self._created = created

    @property
    def roomId(self):
        ''' Spark API roomID property

            :getter: roomId property
            :type: string
        '''
        return self._roomId

    @property
    def personId(self):
        ''' Spark API personId property

            :getter: personId property
            :type: string
        '''
        return self._personId

    @property
    def personEmail(self):
        ''' Spark API personEmail property

            :getter: personEmail property
            :type: string
        '''
        return self._personEmail

    @property
    def personDisplayName(self):
        ''' Spark API personDisplayName property

            :getter: personDisplayName property
            :type: string
        '''
        return self._personDisplayName

    @property
    def personOrgId(self):
        ''' Spark API personOrgId property

            :getter: personOrgId property
            :type: string
        '''
        return self._personOrgId

    @property
    def isModerator(self):
        ''' Spark API isModerator property

            :getter: isModerator property
            :setter: Sets isModerator the property
            :type: bool
        '''
        return self._isModerator

    @isModerator.setter
    def isModerator(self, val):
        assert isinstance(val, bool)
        self.session.put(self.url, json={'isModerator': val})
        return

    @property
    def isMonitor(self):
        ''' Spark API isMonitor property

            :getter: isMonitor property
            :type: bool
        '''
        return self._isMonitor

    @property
    def created(self):
        ''' Spark API created property

            :getter: datetime object representing created time
            :type: datetime.datetime
        '''
        return ts_to_dt(self._created)

    @property
    def room(self):
        ''' Parent room

            :getter: SparkRoom object of parent room
        '''
        return self._parent

    def __repr__(self):
        return f'SparkMembership({self.id})'


class SparkTeamMembership(SparkBase):

    ''' Cisco Spark Team Membership Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param parent: The parent spark team
        :param \**kwargs: All standard Spark API properties of a Team Membership
    '''

    API_BASE = f'{SPARK_API_BASE}team/memberships/'

    def __init__(self,
                 session,
                 id,
                 teamId,
                 personId,
                 personEmail,
                 personDisplayName,
                 personOrgId,
                 isModerator,
                 created,
                 parent=None):

        super().__init__(session, id, 'team/memberships', parent=parent)
        self._teamId = teamId
        self._personId = personId
        self._personEmail = personEmail
        self._personDisplayName = personDisplayName
        self._personOrgId = personOrgId
        self._isModerator = isModerator
        self._created = created

    @property
    def teamId(self):
        ''' Spark API roomID property

            :getter: roomId property
            :type: string
        '''
        return self._teamId

    @property
    def personId(self):
        ''' Spark API personId property

            :getter: personId property
            :type: string
        '''
        return self._personId

    @property
    def personEmail(self):
        ''' Spark API personEmail property

            :getter: personEmail property
            :type: string
        '''
        return self._personEmail

    @property
    def personDisplayName(self):
        ''' Spark API personDisplayName property

            :getter: personDisplayName property
            :type: string
        '''
        return self._personDisplayName

    @property
    def personOrgId(self):
        ''' Spark API personOrgId property

            :getter: personOrgId property
            :type: string
        '''
        return self._personOrgId

    @property
    def isModerator(self):
        ''' Spark API isModerator property

            :getter: isModerator property
            :setter: Sets isModerator the property
            :type: bool
        '''
        return self._isModerator

    @isModerator.setter
    def isModerator(self, val):
        assert isinstance(val, bool)
        self.session.put(self.url, json={'isModerator': val})
        return

    @property
    def isMonitor(self):
        ''' Spark API isMonitor property

            :getter: isMonitor property
            :type: bool
        '''
        return self._isMonitor

    @property
    def created(self):
        ''' Spark API created property

            :getter: datetime object representing created time
            :type: datetime.datetime
        '''
        return ts_to_dt(self._created)

    @property
    def team(self):
        ''' Parent Team

            :getter: SparkTeam object of parent team
        '''
        return self._parent

    def __repr__(self):
        return f'SparkTeamMembership({self.id})'
