# -*- coding: utf-8 -*-

from .base import SparkBase
from .time import SparkTime


class SparkOrganization(SparkBase):

    ''' Cisco Spark Organization Model

        :param \**kwargs: All standard Spark API properties for a Organization
    '''

    api_base = 'https://api.ciscospark.com/v1/organizations/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='organizations', **kwargs)
        else:
            super().__init__(path='organizations', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'displayName': {'type': str,
                                'optional': False,
                                'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False}}

    def __repr__(self):
            return f'SparkOrganization("{self.id}")'

    def __str__(self):
            return f'SparkOrganization({self.displayName})'
