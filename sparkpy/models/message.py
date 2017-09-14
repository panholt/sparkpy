# -*- coding: utf-8 -*-

from .base import SparkBase, SparkProperty
from .time import SparkTime
from .file import SparkFile


class SparkMessage(SparkBase):

    ''' Cisco Spark Message Model

        :param \**kwargs: All standard Spark API properties for a Message
    '''

    API_BASE = 'https://api.ciscospark.com/v1/messages/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'roomId': SparkProperty('roomId'),
                  'roomType': SparkProperty('roomType'),
                  'text': SparkProperty('text', optional=True),
                  'markdown': SparkProperty('markdown', optional=True),
                  'html': SparkProperty('html', optional=True),
                  'personId': SparkProperty('personId'),
                  'personEmail': SparkProperty('personEmail'),
                  'created': SparkProperty('created', cls=SparkTime),
                  'files': SparkProperty('files',
                                         optional=True,
                                         cls=SparkFile),
                  'mentionedPeople': SparkProperty('mentionedPeople',
                                                   optional=True)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='messages', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    def __repr__(self):
            return f'SparkMessage("{self.id}")'

    def __str__(self):
            return f'SparkMessage({self.id})'
