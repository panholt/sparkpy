import base64
from urllib.parse import urlparse
from uuid import UUID, uuid4
from ..constants import SPARK_PATHS, SPARK_URI_B64


def is_uuid(_id):
    ''' Take a string, return True if its a valid uuid 4'''
    try:
        UUID(_id, version=4)
        return True
    except ValueError:
        return False


def is_api_id(_id):
    assert isinstance(_id, str)
    if _id.startswith(SPARK_URI_B64):
        return True
    return False


def api_id_to_uuid(_id):
    assert isinstance(_id, str)
    assert _id.startswith(SPARK_URI_B64)

    url = urlparse(base64.b64decode(_id))
    return url.path.split('/')[-1]


def uuid_to_api_id(path, _id):
    assert isinstance(path, str)
    assert path in SPARK_PATHS
    assert is_uuid(_id) or _id == 'me'

    region = 'us'
    url = f'ciscospark://{region}/{path.upper()}/{_id}'
    url = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    return url.split('=')[0]


def uuid_v4_str():
    return str(uuid4())
