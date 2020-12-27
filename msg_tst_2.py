# we import the Twilio client from the dependency we just installed
from twilio.rest import Client
import os

MSG_KEY = os.environ.get('MSG_KEY')
CLIENT = Client("", MSG_KEY)

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
Client.messages.create(to="13369291348", 
                       from_="8039747673", 
                       body="rtx bot reporting for duty")