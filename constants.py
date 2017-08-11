
# API IDs start with this (base64 encoded cisco://)
SPARK_URI_B64 = 'Y2lzY29zcGFyazovL'

# Spark API Stuff
SPARK_API_VERSION = 1
SPARK_API_BASE = f'https://api.ciscospark.com/v{SPARK_API_VERSION}/'
SPARK_PATHS = ['messages',
               'rooms',
               'people',
               'memberships',
               'team',
               'webhook',
               'organizations',
               'licenses',
               'roles']

# Webhook stuff
WEBHOOK_RESOURCES = ['memberships', 'messages', 'rooms', 'all']
WEBHOOK_EVENTS = ['created', 'updated', 'deleted', 'all']
WEBHOOK_FILTERS = {'memberships': ['roomId', 'personId', 'personEmail', 'isModerator'],
                   'messages': ['roomId', 'roomType', 'personId', 'personEmail', 'mentionedPeople', 'hasFiles'],
                   'rooms': ['type', 'isLocked']}
