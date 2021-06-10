from twilio.rest import Client

CLIENT = Client("account-SID-here", "auth-token-here")

def send_message(to_number, message):
    CLIENT.messages.create(to=to_number, 
                       from_="your-twilio-from-number", 

                       body="rtx bot reporting for duty: " + message)

