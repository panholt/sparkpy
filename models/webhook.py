from .base import SparkBase
from ..constants import SPARK_API_BASE
from ..utils.time import ts_to_dt


class SparkWebhook(SparkBase):

    ''' Cisco Spark Webhook Model

        :param session: SparkSession object
        :type session: `SparkSession`
        :param \**kwargs: All standard Spark API properties for a Webhook
    '''

    API_BASE = f'{SPARK_API_BASE}webhooks/'

    def __init__(self,
                 session,
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

        super().__init__(session, id, 'webhooks')
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

    @property
    def name(self):
        ''' Webhook name

            :getter: Gets the webhook name
            :setter: Set the webhook name
            :type: string
        '''
        return self._name

    @name.setter
    def name(self, val):
        self.session.put(self.url,
                         json={'name': val, 'targetUrl': self.targetUrl})
        self._name = val
        return

    @property
    def targetUrl(self):
        ''' Webhook target url

            :getter: Gets the webhook target url
            :setter: Set the webhook target url
            :type: string
        '''

        return self._targetUrl

    @targetUrl.setter
    def targetUrl(self, val):
        self.session.put(self.url,
                         json={'name': self.name, 'targetUrl': val})
        self._targetUrl = val
        return

    @property
    def resource(self):
        ''' Webhook resource

            https://developer.ciscospark.com/webhooks-explained.html#resources-events

            :getter: Gets the webhook resources
            :type: string
        '''
        return self._resource

    @property
    def event(self):
        ''' Webhook event(s) for the webhook

            https://developer.ciscospark.com/webhooks-explained.html#resources-events

            :getter: Gets the webhook event(s)
            :type: string
        '''
        return self._event

    @property
    def orgId(self):
        ''' orgId of webhook's creater

            :getter: Gets the webhook name
            :type: string
        '''
        return self._orgId

    @property
    def createdBy(self):
        ''' personId of webhook's creater

            :getter: Gets the creater id
            :type: string
        '''
        return self._createdBy

    @property
    def appId(self):
        ''' appId of webhook

            :getter: Gets the appId
            :type: string
        '''
        return self._appId

    @property
    def ownedBy(self):
        ''' personId of webhook's owner

            :getter: Gets the creater id
            :type: string
        '''
        return self._ownedBy

    @property
    def status(self):
        ''' Webhook's status

            :getter: Gets the status
            :type: string
        '''
        return self._status

    @property
    def created(self):
        ''' Webhook created time

            :getter: returns datetime object of webhook creation time
            :type: datetime.datetime
        '''
        return ts_to_dt(self._created)

    @property
    def filter(self):
        ''' Webhook filter(s) for the webhook

            https://developer.ciscospark.com/webhooks-explained.html#resources-events

            :getter: Gets the webhook filter(s)
            :type: string
        '''
        return self._filter

    @property
    def secret(self):
        ''' Webhook event(s) for the webhook

            https://developer.ciscospark.com/webhooks-explained.html#auth

            :getter: Gets the webhook secret
            :type: string
        '''
        return self._secret

    def __repr__(self):
        return f'SparkWebhook({self.id})'
