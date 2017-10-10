# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty
from .time import SparkTime


class SparkOrganization(SparkBase):

    ''' Cisco Spark Organization Model

        :param \**kwargs: All standard Spark API properties for a Organization
    '''

    API_BASE = 'https://api.ciscospark.com/v1/organizations/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'displayName': SparkProperty('displayName'),
                  'created': SparkProperty('created')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='organizations', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    def __repr__(self):
            return f'SparkOrganization("{self.id}")'
