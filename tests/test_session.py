import os
import sys
sys.path.insert(0, os.path.abspath('/Users/panholt/dev/bots/sparkpy/'))
from sparkpy import Spark
from sparkpy.models.container import SparkContainer
token = os.environ['SPARK_DEV_TOKEN']

spark = Spark(token)


def test_headers():
    assert 'Authorization' in spark.session.headers
    assert 'Content-type' in spark.session.headers
    assert spark.session.headers['Authorization'] == 'Bearer ' + token
    assert spark.session.headers['Content-type'] == 'application/json; charset=utf-8'


def test_hooks():
    assert spark.session.hooks.get('response')
    assert len(spark.session.hooks['response']) == 1
    assert spark.session.hooks['response'][0] == spark.session._retry_after_hook


def test_rooms():
    assert isinstance(spark.rooms, SparkContainer)


def test_teams():
    assert isinstance(spark.teams, SparkContainer)


def test_webhooks():
    assert isinstance(spark.webhooks, SparkContainer)
