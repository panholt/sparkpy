from requests.exceptions import JSONDecodeError


class SparkAPIException(Exception):
    ''' Base for Cisco Spark API Errors '''

    def __init__(self, response):
        self.response = response
        super().__init__(self._msg())

    def _msg(self):

        msg = [f'Spark HTTP Response: {self.response.status_code}',
               f'Spark URL: {self.response.request.url}']
        if self.response.request.body:
            msg.append(f'Payload: {self.request.body}')
        try:
            data = self.response.json()
            msg.append(data.get('message'))
            msg.append(data.get('trackingId'))

            for error in data.get('errors', []):
                if error['description'] not in data.get('message'):
                    msg.append(f'Further details: {error}')

        except JSONDecodeError:
            pass
        return ' '.join(msg)


# Specific exceptions below are for catching purposes.

# ---------------------! Rooms
# class SparkRoomNotFoundError(SparkAPIException):
#     '''
#     Exception raised when a Spark Room is not found
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkRoomTitleEmptyError(SparkAPIException):
#     '''
#     Exception raised when a Spark Room is created
#     but the title property is left blank
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkRoomsError(SparkAPIException):
#     '''
#     Exception raised when a Spark Rooms API method returns an error
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# # ---------------------!  Messages
# class SparkMessageTooLongError(SparkAPIException):
#     '''
#     Exception raised when a Spark Message exceeds the maximum length
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkMentionedUserNotInRoomError(SparkAPIException):
#     '''
#     Exception raised when a Spark Message contains an @mention but the
#         but the mentioned user is not in the room
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkMessageNotFoundError(SparkAPIException):
#     '''
#     Exception raised when a Spark Message is not found
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkMessageErrorError(SparkAPIException):
#     '''
#     Exception raised when a Spark Message API method returns an error
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# # ---------------------!  Teams

# class SparkTeamNotFoundError(SparkAPIException):
#     '''
#     Exception raised when a Spark Team is not found
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkTeamsError(SparkAPIException):
#     '''
#     Exception raised when a Spark Teams API method returns an error
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# # ---------------------!  Memberships

# class SparkMembershipNotFoundError(SparkAPIException):
#     '''
#     Exception raised when a Spark Membership is not found
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkModeratorMissingEntitlementError(SparkAPIException):
#     '''
#     Exception raised when a user tries to assign a moderator,
#         but the account is not paid.
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkMembershipError(SparkAPIException):
#     '''
#     Exception raised when a Spark Message API method returns an error
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkUserAlreadyInRoomError(SparkAPIException):
#     '''
#     Exception raised when a Spark user is added
#     to a room that they are already a member of
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# # ---------------------!  Webhooks
# class SparkWebhookError(SparkAPIException):
#     '''
#     Exception raised when a Spark Webhook API method returns an error
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# class SparkWebhookNotFound(SparkAPIException):
#     '''
#     Exception raised when a Spark Team is not found
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass


# # ---------------------!  Generics
# class SparkAuthError(SparkAPIException):
#     '''
#     Exception raised when a Spark authorization error
#     Attributes:
#         message -- explanation of the error
#         response -- Requests response object
#     '''
#     pass
