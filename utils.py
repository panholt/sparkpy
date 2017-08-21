import base64
from urllib.parse import urlparse
from uuid import UUID, uuid4

spark_paths = ['messages',
               'rooms',
               'people',
               'memberships',
               'teams',
               'team/memberships',
               'webhook',
               'organizations',
               'licenses',
               'roles']

magic_number = 'Y2lzY29zcGFyazovL'  # Magic number: b64.encode('ciscospark://')


# -------------! uuid helpers
def is_uuid(_id):
    ''' Take a string, return True if its a valid uuid 4'''
    try:
        UUID(_id, version=4)
        return True
    except ValueError:
        return False


def decode_api_id(_id):
    if _id.startswith(magic_number):
        __id = _id
        # Avoid padding errors from base64
        padding = len(_id) % 4
        if padding:
            _id += '=' * (4 - padding)
        url = urlparse(base64.urlsafe_b64decode(_id)).decode()
        uuid = url.path.split('/')[-1]
        path = url.path.split('/')[1].lower()
        return {'uuid': uuid,
                'path': path.replace('_', '/') + 's',
                'id': __id}
    else:
        raise ValueError('Invalid API ID')


def is_api_id(_id, path=''):
    ''' TODO docs '''
    try:
        decode_api_id(_id)
        return True
    except ValueError:
        return False


def api_id_to_uuid(_id):
    ''' TODO docs '''
    assert isinstance(_id, str)
    assert _id.startswith(magic_number)

    url = urlparse(base64.b64decode(_id))
    return url.path.split('/')[-1]


def uuid_to_api_id(path, _id):
    ''' TODO docs '''
    # 'me' and 'consumer' are the only (known) non uuid values
    assert is_uuid(_id) or _id == 'me' or _id == 'consumer'

    region = 'us'  # Are there others??
    url = f'ciscospark://{region}/{path.upper()}/{_id}'
    url = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    return url.split('=')[0]


def uuid_v4_str():
    ''' TODO docs '''
    return str(uuid4())

