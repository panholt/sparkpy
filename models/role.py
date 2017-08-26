# -*- coding: utf-8 -*-

from .base import SparkBase


class SparkRole(SparkBase):

    ''' Cisco Spark Role Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    api_base = 'https://api.ciscospark.com/v1/roles/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='roles', **kwargs)
        else:
            super().__init__(path='roles', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'name': {'type': str,
                         'optional': False,
                         'mutable': False}}

    def __repr__(self):
            return f'SparkRole("{self.id}")'

    def __str__(self):
            return f'SparkRole({self.name})'
