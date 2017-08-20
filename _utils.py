from .session import SparkSession
from .models.room import SparkRoom
from .models.people import SparkPerson
from .models.team import SparkTeam


def is_api_id(_id, path):
    pass


def create_room(title, team_id=None):
    '''Create a Cisco Spark room

            :param title: Room title
            :type title: str

            :return: SparkTeam
        '''

    data = {'title': title}
    if team_id:
        assert is_api_id(team_id, 'team')
        data['teamId'] = team_id
    with SparkSession() as s:
        room = s.post('rooms', json=data).json()
    return SparkRoom(**room)


def create_one_on_one_room(person, message):
    '''Create or send a message to a 1:1 room

            :param person: Either a personId, email address, or API id
            :type person: str

            :return: SparkRoom
        '''

    isinstance(message, str) and len(message) > 0
    if isinstance(person, SparkPerson) or is_api_id(person):
        message = send_message(message, person_id=person.id)
    elif '@' in person:
        message = send_message(message, person_email=person)
    else:
        raise ValueError('Person must be an email address, SparkPerson, \
                         or Spark API ID')
    return message.room


def create_team(self, name):
    '''Create a Cisco Spark webhook

            :param name: Team name
            :type name: str

            :return: SparkTeam
        '''

    team = self.post('teams', json={'name': name})
    return SparkTeam(self, **team.json())


def create_webhook(self,
                   name,
                   target_url,
                   resource,
                   event,
                   filter=None,
                   secret=None):
    '''Create a Cisco Spark webhook

            :param name: Webhook name
            :type name: str

            :param target_url: Sets the `targetUrl` property
            :type target_url: str

            :param resource: Sets the `resource` property
            :type resource: str

            :param event: Sets the `event` property
            :type event: str

            :param person_id: Sets the `toPersonId` property
            :type person_id: str

            :param filter: Sets the `filter` property
            :type filter: str

            :param secret: Sets the `secret` property
            :type secret: str

            :return: SparkWebhook

            :raises: AssertionError
        '''

    assert resource in WEBHOOK_RESOURCES
    assert event in WEBHOOK_EVENTS
    data = {'name': name,
            'targetUrl': target_url,
            'resource': resource,
            'event': event}
    if filter:
        assert any([filter.starswith(item)
                    for item in WEBHOOK_FILTERS[resource]])
        data['filter'] = filter
    if secret:
        data['secret'] = secret
    webhook = self.post('webhooks', json=data)
    return SparkWebhook(**webhook.json())


def send_message(text,
                 room_id=None,
                 person_id=None,
                 person_email=None,
                 file=None):
    '''Send a Cisco Spark message

        :param text: Markdown formatted message body
                     If message is longer than 7,000 characters
                     it is split at linebreak boundries
                     and sent as seperate messages
        :type text: str
        :param room_id: Sets the `roomId` property
        :type room_id: str
        :param person_id: Sets the `toPersonId` property
        :type person_id: str
        :param person_email: Sets the `toPersonEmailAddress` property
        :type person_id: str
        :param file: Path to file to upload
        :type file: str

        :return: None
        :raises ValueError: when none of 'room_id', 'person_id',
                            or 'person_email' are provided

        .. note:: This method must be called with exactly one of
                  'room_id', 'person_id', 'person_email'
    '''

    base_data = {}
    if room_id:
        assert is_api_id(room_id)
        base_data['roomId'] = room_id
    elif person_id:
        assert is_api_id(person_id)
        base_data['toPersonId'] = person_id
    elif person_email:
        assert '@' in person_email
        base_data['toPersonEmail'] = person_email
    else:
        raise ValueError('Must provide either a roomId, personId, \
                         or email address')

    with SparkSession() as s:
        while len(text) > 7000:  # Technically 7439
            split_idx = text.rfind('\n', 1, 6999)
            if split_idx == -1:
                split_idx = 7000
            data = {'markdown': text[:split_idx]}
            data.update(base_data)
            if file:
                s.__send_file(file, data)
                file = None
            else:
                s.post('messages', json=data)
            text = text[split_idx:]
        else:
            data = {'markdown': text}
            data.update(base_data)
            if file:
                s.__send_file(file, data)
                return
            s.post('messages', json=data)
        return
