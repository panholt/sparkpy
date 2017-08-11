from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkWebhook(object):

    API_BASE = f'{SPARK_API_BASE}webhooks/'

    def __init__(self,
                 spark,
                 id,
                 name,
                 targetUrl,
                 resource,
                 event,
                 orgId,
                 createdBy,
                 appId,
                 ownedBy,
                 status,
                 created,
                 filter=None,
                 secret=None):

        self._id = id
        self._name = name
        self._targetUrl = targetUrl
        self._resource = resource
        self._event = event
        self._orgId = orgId
        self._createdBy = createdBy
        self._appId = appId
        self._ownedBy = ownedBy
        self._status = status
        self._created = created
        self._filter = filter
        self._secret = secret
        self._path = 'webhooks'
        self._url = f'{SPARK_API_BASE}{self.path}/{self.id}'

        @property
        def id(self):
            return self._id

        @property
        def name(self):
            return self._name

        @property
        def targetUrl(self):
            return self._targetUrl

        @property
        def resource(self):
            return self._resource

        @property
        def event(self):
            return self._event

        @property
        def orgId(self):
            return self._orgId

        @property
        def createdBy(self):
            return self._createdBy

        @property
        def appId(self):
            return self._appId

        @property
        def ownedBy(self):
            return self._ownedBy

        @property
        def status(self):
            return self._status

        @property
        def created(self):
            return ts_to_dt(self._created)

        @property
        def filter(self):
            return self._filter

        @property
        def secret(self):
            return self._secret

        def update(self, name=self.name, targetUrl=self.targetUrl):
            self.spark.put(self.url,
                           json={'name': name, 'targetUrl': targetUrl})

        def delete(self):
            self.spark.delete(self.url)

        def __repr__(self):
            return f'SparkWebhook({self.id})'
