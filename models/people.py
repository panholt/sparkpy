from .base import SparkBase
from ..utils.time import ts_to_dt
from ..constants import SPARK_API_BASE


class SparkPerson(SparkBase):

    API_BASE = f'{SPARK_API_BASE}people/'

    def __init__(self,
                 spark,
                 id,
                 emails,
                 displayName,
                 avatar,
                 orgId,
                 created,
                 type,
                 firstName=None,  # ----!Optional properties
                 lastName=None,
                 nickName=None,
                 lastActivity=None,
                 status=None,
                 licenses=[],
                 roles=[],
                 timezone=None,
                 invitePending=False,
                 loginEnabled=True):

        super().__init__(id, 'people')
        self.spark = spark
        self._emails = emails
        self._displayName = displayName
        self._firstName = firstName
        self._lastName = lastName
        self._nickName = nickName
        self._avatar = avatar
        self._orgId = orgId
        self._created = created
        self._lastActivity = lastActivity
        self._status = status
        self._type = type
        self._licenses = licenses
        self._roles = roles
        self._timezone = timezone
        self._invitePending = invitePending
        self._loginEnabled = loginEnabled

    @property
    def emails(self):
        # Emails is returned as an array but will only ever have one entry
        # For now anyway
        return self._emails[0]

    @property
    def displayName(self):
        return self._displayName

    @property
    def firstName(self):
        return self._firstName

    @property
    def lastName(self):
        return self._lastName

    @property
    def nickName(self):
        return self._nickName

    @property
    def avatar(self):
        return self._avatar

    @property
    def orgId(self):
        return self._orgId

    @property
    def licenses(self):
        return self._licenses

    @property
    def created(self):
        return ts_to_dt(self._created)

    @property
    def lastActivity(self):
        if self._lastActivity:
            return ts_to_dt(self._lastActivity)

    @property
    def status(self):
        return self._status

    @property
    def type(self):
        return self._type

    def delete(self):
        self.spark.delete(self.url)
        return

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
        existing_data = self.get(self.url).json()
        data = existing_data.update(updates)
        self.spark.put(self.url, json=data)
        return

    def __repr__(self):
        return f'SparkPerson{self.id})'
