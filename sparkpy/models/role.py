# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty


class SparkRole(SparkBase):

    ''' Cisco Spark Role Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/roles/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'name': SparkProperty('name')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='roles', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    def __repr__(self):
            return f'SparkRole("{self.id}")'

    def __str__(self):
            return f'SparkRole({self.name})'
