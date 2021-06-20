# 3080Plx
Definitely not my custom made web scraper bot for buying an RTX 3080. Nope definitely not that. 

SETUP:
1. If using Chrome:
    Download ChromeDriver from https://chromedriver.chromium.org/downloads and add the .exe path to the settings.json file
2. If using FireFox:
    Download GeckoDriver from here: https://github.com/mozilla/geckodriver/releases  and add it to your PATH environment variables.
3. Add your information to the 'settings.json' file.
4. Install requirements from requirements.txt with ```pip install -r requirements.txt```
5. If you want to use this bot and have it text you when it gets a hit. You will need to make a developer account on Twilio and add your private keys to the mssage.py class.
  Like this:
  ```CLIENT = Client("Account SID", "Auth Token")```
    You can disable messaging in the settings file if you want.
6. To Run: ```py app.py``` in the command line



