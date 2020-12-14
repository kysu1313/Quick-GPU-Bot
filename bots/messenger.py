from twilio.rest import Client

CLIENT = Client("ACce6e26e6caff712faff02f0ea8bab413", "c09931d89b55c4275650b96848fc1a99")

def send_message(to_number, message):
    CLIENT.messages.create(to=to_number, 
                       from_="8039747673", 
                       body="rtx bot reporting for duty: " + message)

