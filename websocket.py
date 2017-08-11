import json
import websocket
import logging
from .utils import uuid, uuid_to_api_id

log = logging.getLogger('pyspark.websocket')

class SparkWebsocket(websocket.WebSocketApp):

    def __init__(self, wss_url, message_callback, rooms_callback, bearer_token=None):
        if not bearer_token:
            try:
                bearer_token = os.environ['SPARK_TOKEN']
            except KeyError:
                raise Exception('SparkWebsocket Requires a bearer token')
        self._wss_url = wss_url
        self._last_ping_id = ''
        self._rooms_callback = rooms_callback
        self._message_callback = message_callback
        super().__init__(self._wss_url,
                         on_open = self._open_cb,
                         on_message = self._message_callback,
                         on_close = self._close_cb,
                         on_ping = self._ping_cb,
                         on_error = self._error_cb)

    @property
    def wss_url(self):
        return self._wss_url

    @property
    def last_ping_id(self):
        return self._last_ping_id

    @last_ping_id.setter
    def last_ping_id(self, val):
        self._last_ping_id = val
        return

    @property
    def rooms_callback(self):
        return self._rooms_callback
    
    @property
    def message_callback(self):
        return self._message_callback

    def _open_cb(self, ws):
        log.info('Websocket connected')
        data = {'id': uuid(),
                'type': 'authorization',
                'data': {'token': 'Bearer ' + self.token}}
        data = json.dumps(data)
        log.debug('Sending: %s', data)
        ws.send(data)
        self._spark_ping()
        return

    def _open_cb(self, ws):
        log.info('Websocket connected')
        data = {'id': uuid(),
                'type': 'authorization',
                'data': {'token': 'Bearer ' + self.token}}
        data = json.dumps(data)

        log.debug('Sending: %s', data)
        ws.send(data)
        self._spark_ping()
        return

    def _message_cb(self, ws, message):
        try:
            event = json.loads(message)
            log.debug('Received event on websocket: %s', event)
            # Handle pings
            if event.get('type') == 'pong':
                if event.get('id') != self._last_ping_id:
                    raise Exception('Ping ID does not match')
                return
            else:
                event_type = event['data'].get('eventType')

            # Typing indicators
            if 'typing' in event_type:
                # We have no use for these so ignore them.
                return

            # Conversation Service
            elif event_type == 'conversation.activity':
                verb = event['data']['activity']['verb']
                if verb == 'post':
                    _id = uuid_to_api_id('messages', event['data']['activity']['id'])
                    self._message_callback(_id)
                elif verb == 'acknowledge':
                    # read receipt, ignore
                    return
                elif verb == 'create':
                    _id = uuid_to_api_id('rooms', event['data']['activity']['id'])
                    self._rooms_callback(_id)
                elif verb == 'leave':
                    _id = uuid_to_api_id('rooms', event['data']['activity']['id'])
                    self._rooms_callback(_id, leave=True)
                elif verb == 'add':
                    if 'TEAM' in event['data']['activity']['target']['tags']:
                        # Team subroom create.
                        return
                    else:
                        # Added to room
                        _id = uuid_to_api_id('rooms', event['data']['activity']['target']['id'])
                        self._rooms_callback(_id)

                elif verb == 'update':
                    _id = uuid_to_api_id('rooms', event['data']['activity']['target']['id'])
                    self._rooms_callback(_id)
                else:
                    log.warning('Unknown verb: %s', verb)
            else:
                print('Unknown event type: {}'.format(event_type))
        except ValueError:
            pass
        return

    def _error_cb(self, ws, error):
        raise error

    def _close_cb(self, ws):
        log.info('Websocket connection closed')
        return

    def _ping_cb(self, ws, data):
        log.debug('_ping_cb hit, sending ping')
        self._spark_ping()
        return

    def _spark_ping(self):
        self._last_ping_id = str(uuid.uuid4())
        data = json.dumps({'type': 'ping', 'id': self._last_ping_id})
        log.debug('Sending: %s', data)
        self.app.send(data)
        return

    def __repr__(self):
        return 'SparkWebsocket({})'.format(self.wss_url)