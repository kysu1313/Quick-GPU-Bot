from twilio.rest import Client

CLIENT = Client("your-UID-here", "your-API-key-here")

def send_message(to_number, message):
    CLIENT.messages.create(to=to_number, 
                       from_="your-twilio-number-here", 
                       body="rtx bot reporting for duty: " + message)

