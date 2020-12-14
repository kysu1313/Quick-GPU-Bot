# we import the Twilio client from the dependency we just installed
from twilio.rest import Client




# the following line needs your Twilio Account SID and Auth Token
client = Client("ACce6e26e6caff712faff02f0ea8bab413", "c09931d89b55c4275650b96848fc1a99")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="13369291348", 
                       from_="8039747673", 
                       body="rtx bot reporting for duty")