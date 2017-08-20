# -*- coding: utf-8 -*-

from .base import SparkBase


class SparkLicense(SparkBase):

    ''' Cisco Spark License Model

        :param \**kwargs: All standard Spark API properties for a License
    '''

    API_BASE = 'https://api.ciscospark.com/v1/licenses/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='licenses', **kwargs)
        else:
            super().__init__(path='licenses', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'name': {'type': str,
                         'optional': False,
                         'mutable': False},
                'totalUnits': {'type': int,
                               'optional': False,
                               'mutable': False},
                'consumedUnits': {'type': int,
                                  'optional': False,
                                  'mutable': False}}

    def __repr__(self):
            return f'SparkLicense("{self.id}")'

    def __str__(self):
            return f'SparkLicense({self.name})'
