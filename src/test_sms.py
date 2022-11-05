# Download the helper library from https://www.twilio.com/docs/python/install
# import os
from twilio.rest import Client

# Find your Account SID and Auth Token in Account Info and set the environment variables.
# See http://twil.io/secure

# account_sid = os.environ['AC9f7e889c258470bae55da4c8e326abc0']
# auth_token = os.environ['3606037c7aa5d38a56f1e11a519ae578']
account_sid = 'AC9f7e889c258470bae55da4c8e326abc0'
auth_token = '3606037c7aa5d38a56f1e11a519ae578'
client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Hi there',
    from_='+12538678817',
    to='+13062800816'
)

print(message.sid)
