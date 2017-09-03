'''
sparkpy.utils
~~~~~~~~~~~~~~
Utility functions that are used internally by sparkpy
'''

import base64
from urllib.parse import urlparse
from uuid import UUID, uuid4


# Shortcuts to translate between internal API paths
# and the external url paths
url2api = {'messages': 'MESSAGE',
           'rooms': 'ROOM',
           'people': 'PEOPLE',
           'memberships': 'MEMBERSHIP',
           'teams': 'TEAM',
           'team/memberships': 'TEAM_MEMBERSHIP',
           'webhook': 'WEBHOOK',
           'organizations': 'ORGANIZATION',  # Unsure about these
           'licenses': 'LICENSE',
           'roles': 'ROLE'}

api2url = {'MESSAGE': 'messages',
           'ROOM': 'rooms',
           'PEOPLE': 'people',
           'MEMBERSHIP': 'memberships',
           'TEAM': 'teams',
           'TEAM_MEMBERSHIP': 'team/memberships',
           'WEBHOOK': 'webhook',
           'ORGANIZATION': 'organizations',  # Unsure about these
           'LICENSE': 'licenses',
           'ROLE': 'roles'}

# Magic number: b64.encode('ciscospark://')
magic_number = 'Y2lzY29zcGFyazovL'


def add_padding(_id):
    ''' Properly pad base64 strings from Cisco Spark API '''
    padding = len(_id) % 4
    if padding:
        _id += '=' * (4 - padding)
    return _id


# -------------! uuid helpers
def is_uuid(_id):
    ''' Take a string, return True if its a valid uuid 4'''
    # Handle consumer org
    if _id == 'consumer':
        return True
    try:
        # Handle memberships
        if ':' in _id:
            _id, parent = _id.split(':')
            UUID(parent, version=4)
        UUID(_id, version=4)
        return True
    except ValueError:
        return False


def decode_api_id(_id):
    ''' Takes a Cisco Spark API ID and returns a dictonary of the components
        :raises: `ValueError`
    '''
    if _id.startswith(magic_number):
        __id = _id
        url = urlparse(base64.b64decode(add_padding(_id))).decode()
        uuid = url.path.split('/')[-1]
        path = url.path.split('/')[1]
        return {'uuid': uuid,
                'path': api2url[path],
                'id': __id}
    else:
        raise ValueError('Invalid API ID')


def is_api_id(_id, path=None):
    ''' Returns `True` if provided with a valid Cisco Spark API ID
        An optional `path` may be specified to validate the object
        is of the correct type

        :raises: `ValueError`
    '''
    try:
        result = decode_api_id(_id)
        if result:
            if path and path != result['path']:
                return True
        return True
    except ValueError:
        return False


def api_id_to_uuid(_id):
    ''' Takes Cisco Spark API ID and returns the uuid for the object'''
    if not isinstance(_id, str) or not _id.startswith(magic_number):
        raise ValueError('Invalid Cisco Spark API id provided')

    url = urlparse(base64.b64decode(add_padding(_id)))
    return url.path.split(b'/')[-1].decode('utf-8')


def uuid_to_api_id(_id, path):
    ''' Takes a path (ie: messages) and a uuid
        to generate a Cisco Spark API ID '''

    # memberships are actually two uuids {resource}:{id}
    parent = None
    if 'MEMBERSHIP' in path:
        if ':' not in _id:
            raise ValueError(f'{path} requires two uuids seperated by a colon')
        else:
            parent, _id = _id.split(':')
            if not is_uuid(parent):
                raise ValueError('Invalid UUID for parent Team/Room')
    # 'consumer' is the only (known) non uuid values
    if not is_uuid(_id) and _id != 'consumer':
        raise ValueError('Invalid UUID provided')
    if path in url2api:
        path = url2api[path]
    elif path not in api2url:
        raise ValueError('Invalid Path specified')

    if parent:
        _id = f'{parent}:{_id}'
    region = 'us'  # Are there others??
    url = f'ciscospark://{region}/{path}/{_id}'
    url = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    return url.split('=')[0]


def uuid_v4_str():
    ''' Returns a valid uuidv4 string'''
    return str(uuid4())
