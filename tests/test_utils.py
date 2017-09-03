import pytest
import os
import sys
sys.path.insert(0, os.path.abspath('/Users/panholt/dev/bots/sparkpy/'))
from sparkpy.utils import *

test_data = {'message': {'id': 'Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk',
                         'uuid': '92db3be0-43bd-11e6-8ae9-dd5b3dfc565d',
                         'path': 'MESSAGE'},
             'person': {'id': 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY',
                        'uuid': 'f5b36187-c8dd-4727-8b2f-f9c447f29046',
                        'path': 'PEOPLE'},
             'room': {'id': 'Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0',
                      'uuid': 'bbceb1ad-43f1-3b58-9147-f14bb0c4d154',
                      'path': 'ROOM'},
             'membership': {'id': 'Y2lzY29zcGFyazovL3VzL01FTUJFUlNISVAvMGQwYzkxYjYtY2U2MC00NzI1LWI2ZDAtMzQ1NWQ1ZDExZWYzOmNkZTFkZDQwLTJmMGQtMTFlNS1iYTljLTdiNjU1NmQyMjA3Yg',
                            'uuid': '0d0c91b6-ce60-4725-b6d0-3455d5d11ef3:cde1dd40-2f0d-11e5-ba9c-7b6556d2207b',
                            'path':'MEMBERSHIP'},
             'team': {'id': 'Y2lzY29zcGFyazovL3VzL1RFQU0vMTNlMThmNDAtNDJmYy0xMWU2LWE5ZDgtMjExYTBkYzc5NzY5',
                            'uuid': '13e18f40-42fc-11e6-a9d8-211a0dc79769',
                            'path':'TEAM'},
             'team_membership': {'id': 'Y2lzY29zcGFyazovL3VzL1RFQU1fTUVNQkVSU0hJUC8wZmNmYTJiOC1hZGNjLTQ1ZWEtYTc4Mi1lNDYwNTkyZjgxZWY6MTNlMThmNDAtNDJmYy0xMWU2LWE5ZDgtMjExYTBkYzc5NzY5',
                            'uuid': '0fcfa2b8-adcc-45ea-a782-e460592f81ef:13e18f40-42fc-11e6-a9d8-211a0dc79769',
                            'path':'TEAM_MEMBERSHIP'},
             'webhook': {'id': 'Y2lzY29zcGFyazovL3VzL1dFQkhPT0svZjY0ZDViNTQtOTg4YS00YmU5LWE1ODItMjM5MzcyZWI4M2Mw',
                            'uuid': 'f64d5b54-988a-4be9-a582-239372eb83c0',
                            'path':'WEBHOOK'},
             'organization': {'id': 'Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE',
                            'uuid': '96abc2aa-3dcc-11e5-a152-fe34819cdc9a',
                            'path':'ORGANIZATION'},
             'consumer_org': {'id': 'Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi9jb25zdW1lcg',
                            'uuid': 'consumer',
                            'path':'ORGANIZATION'},
             }

def test_is_uuid():
    uuid = 'f5b36187-c8dd-4727-8b2f-f9c447f29046'
    assert is_uuid(uuid)
    assert is_uuid('NOT A UUID') is False
    return

def test_decode_api_id():
    for value in test_data.values():
        result = decode_api_id(value['id'])
        assert result['id'] == value['id']
        assert url2api[result['path']] == value['path']
        assert result['uuid'] == value['uuid']
    with pytest.raises(ValueError):
        decode_api_id('INCORRECT VALUE')
    return

def test_is_api_id():
    for value in test_data.values():
        assert is_api_id(value['id'])

def test_api_id_to_uuid():
    for value in test_data.values():
        uuid = api_id_to_uuid(value['id'])
        assert is_uuid(uuid)
        assert uuid == value['uuid']
    with pytest.raises(ValueError):
        api_id_to_uuid('INCORRECT VALUE')

def test_uuid_to_api_id():
    for value in test_data.values():
        api_id = uuid_to_api_id(value['uuid'], value['path'])
        assert api_id == value['id']
    with pytest.raises(ValueError):
        uuid_to_api_id('INCORRECT', 'VALUES')


