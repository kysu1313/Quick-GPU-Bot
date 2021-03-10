from twilio.rest import Client

CLIENT = Client("Client Key", "client secret")

def send_message(to_number, message):
    CLIENT.messages.create(to=to_number, 
                       from_="8039747673", 
                       body="rtx bot reporting for duty: " + message)

