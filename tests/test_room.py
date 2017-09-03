import os
import sys
sys.path.insert(0, os.path.abspath('/Users/panholt/dev/bots/sparkpy/'))
from datetime import datetime
from sparkpy import Spark
from sparkpy.models.room import SparkRoom
from sparkpy.utils import uuid_v4_str


TOKEN = os.environ['SPARK_DEV_TOKEN']
ID = 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wYmEyODA5NC02OTBjLTRiODMtODBlOS1hYTc0ZTEyZTk5MDM'
UUID = uuid_v4_str()
ROOM = None
spark = Spark(TOKEN)


def test_room_create():
    ts = datetime.now().isoformat()
    start_length = len(spark.rooms)
    room = spark.create_room(f'{UUID}:{ts}')
    assert isinstance(room.id, str)
    assert room.title == f'{UUID}:{ts}'
    assert len(room.messages) == 0
    assert len(room.members) == 1
    # Dummy call to refresh the rooms
    spark.rooms[-1]
    stop_length = len(spark.rooms)
    assert start_length == stop_length - 1
    global ROOM
    ROOM = room.id
    return


def test_room_rename():
    room = spark.rooms[ROOM]
    old_title = room.title
    room.title = old_title[::-1]
    assert room.title == old_title[::-1]
    return


def test_add_person_by_email():
    room = spark.rooms[ROOM]
    room.add_person_by_email('panholt@gmail.com')
    assert any((person.personEmail == 'panholt@gmail.com'
               for person in room.members))
    return


def test_remove_person_by_email():
    room = spark.rooms[ROOM]
    room.remove_person_by_email('panholt@gmail.com')
    assert all((person.personEmail != 'panholt@gmail.com'
               for person in room.members))
    return


def test_add_person_by_id():
    room = spark.rooms[ROOM]
    room.add_person_by_id(ID)
    assert any((person.personId == ID
               for person in room.members))
    return


def test_remove_person_by_id():
    room = spark.rooms[ROOM]
    room.remove_person_by_id(ID)
    assert all((person.personId != ID
               for person in room.members))
    return


def test_room_find():
    room_search = []
    for room in spark.rooms.find('title', UUID):
        room_search.append(room)
    assert len(room_search) == 1


def test_room_filtered():
    room_search = []
    for room in spark.rooms.filtered(lambda x: UUID in x.title):
        room_search.append(room)
    assert len(room_search) == 1
