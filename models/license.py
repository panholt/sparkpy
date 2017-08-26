from .base import SparkBase, SparkProperty


class SparkLicense(SparkBase):

    ''' Cisco Spark License Model

        :param \**kwargs: All standard Spark API properties for a License
    '''

    API_BASE = 'https://api.ciscospark.com/v1/licenses/'
    PROPERTIES = {'id': SparkProperty('id'),
                  'name': SparkProperty('name'),
                  'totalUnits': SparkProperty('totalUnits'),
                  'consumedUnits': SparkProperty('consumedUnits')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, path='licenses', **kwargs)

    def update():
        raise NotImplemented(f'{self} is readonly')

    def __repr__(self):
            return f'SparkLicense("{self.id}")'

    def __str__(self):
            return f'SparkLicense({self.name})'
