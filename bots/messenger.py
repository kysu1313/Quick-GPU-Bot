import telebot 
from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon import TelegramClient, sync, events 

class Bot():

    def __init__(self):
        self.API_ID = "1731805"
        self.API_HASH = "8dad59f0d88fe2523377802cc841edf7"
        self.API_TOKEN = "1401658145:AAFBQy82afRWa3RlB8zriUT29yO2aUyjPlY"
        self.client = TelegramClient('session', self.API_ID, self.API_HASH)

    def login(self, number):
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(number)
            self.client.sign_in(number, input('Enter the code: '))

    def send_message(self, message):
        # self.client = TelegramClient('session', self.API_ID, self.API_HASH)
        # self.client.connect()
        # if not client.is_user_authorized():
        #     client.send_code_request(number)
        #     client.sign_in(number, input('Enter the code: '))

        try:
            reciever = InputPeerUser('user_id', 'user_hash')
            self.client.send_message("@kysu3376", reciever, message, parse_mode='html')
        except Exception as e:
            print(e)

    def drop_connection(self):
        self.client.disconnect()