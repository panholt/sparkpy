# -*- coding: utf-8 -*-

from .base import SparkBase
from .time import SparkTime
from .file import SparkFile


class SparkMessage(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/messages/'

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(args[0], path='messages', **kwargs)
        else:
            super().__init__(path='messages', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    @property
    def properties(self):
        return {'id': {'type': str,
                       'optional': False,
                       'mutable': False},
                'roomId': {'type': str,
                           'optional': False,
                           'mutable': False},
                'roomType': {'type': str,
                             'optional': False,
                             'mutable': False},
                'text': {'type': str,
                         'optional': False,
                         'mutable': False},
                'markdown': {'type': str,
                             'optional': True,
                             'mutable': False},
                'personId': {'type': str,
                             'optional': False,
                             'mutable': False},
                'personEmail': {'type': str,
                                'optional': False,
                                'mutable': False},
                'created': {'type': SparkTime,
                            'optional': False,
                            'mutable': False},
                'files': {'type': SparkFile,
                          'optional': True,
                          'mutable': False}}
