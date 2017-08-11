# Base Class
class SparkException(Exception):
    def __init__(self, response):
        self.response = response
        self.message = self._message()
        super(SparkException, self).__init__(self.message)

    def _message(self):
        try:
            data = self.response.json()
            message = data.get('message', 'Not Found')
            tracking_id = data.get('trackingId', 'Not Found')

            msg = f'\nSpark HTTP Response: {self.response.status_code}'
            msg += f'\nSpark URL: {self.response.request.url}'
            msg += f'\nPayload Sent: {str(self.response.request.body)}'
            msg += f'\nMessage: {message}'
            msg += f'\nTracking ID: {tracking_id}'

            for error in data.get('errors', []):
                if error['description'] not in message:
                    msg += f'\nFurther details: {error}'

        except ValueError:  # We're in an outage or something things are jacked
            msg = 'Spark API Returned invalid JSON'
        return msg


# Specific exceptions below are for catching purposes.

# ---------------------! Rooms
class SparkRoomNotFoundError(SparkException):
    '''
    Exception raised when a Spark Room is not found
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkRoomTitleEmptyError(SparkException):
    '''
    Exception raised when a Spark Room is created
    but the title property is left blank
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkRoomsError(SparkException):
    '''
    Exception raised when a Spark Rooms API method returns an error
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


# ---------------------!  Messages
class SparkMessageTooLongError(SparkException):
    '''
    Exception raised when a Spark Message exceeds the maximum length
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkMentionedUserNotInRoomError(SparkException):
    '''
    Exception raised when a Spark Message contains an @mention but the
        but the mentioned user is not in the room
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkMessageNotFoundError(SparkException):
    '''
    Exception raised when a Spark Message is not found
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkMessageErrorError(SparkException):
    '''
    Exception raised when a Spark Message API method returns an error
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


# ---------------------!  Teams

class SparkTeamNotFoundError(SparkException):
    '''
    Exception raised when a Spark Team is not found
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkTeamsError(SparkException):
    '''
    Exception raised when a Spark Teams API method returns an error
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


# ---------------------!  Memberships

class SparkMembershipNotFoundError(SparkException):
    '''
    Exception raised when a Spark Membership is not found
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkModeratorMissingEntitlementError(SparkException):
    '''
    Exception raised when a user tries to assign a moderator,
        but the account is not paid.
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkMembershipError(SparkException):
    '''
    Exception raised when a Spark Message API method returns an error
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkUserAlreadyInRoomError(SparkException):
    '''
    Exception raised when a Spark user is added
    to a room that they are already a member of
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


# ---------------------!  Webhooks
class SparkWebhookError(SparkException):
    '''
    Exception raised when a Spark Webhook API method returns an error
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


class SparkWebhookNotFound(SparkException):
    '''
    Exception raised when a Spark Team is not found
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass


# ---------------------!  Generics
class SparkAuthError(SparkException):
    '''
    Exception raised when a Spark authorization error
    Attributes:
        message -- explanation of the error
        response -- Requests response object
    '''
    pass
