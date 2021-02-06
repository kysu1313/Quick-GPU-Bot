from twilio.rest import Client

# You need to create an account on https://www.twilio.com/docs/usage/api and add your tokens
CLIENT = Client("account-sid-goes-here", "auth-token-goes-here")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number


def send_message(to_number, message):
    CLIENT.messages.create(to=to_number,
                           from_="8039747673",
                           body="rtx bot reporting for duty: " + message)
