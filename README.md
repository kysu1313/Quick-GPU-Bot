# 3080Plx
Definitely not my custom made web scraper bot for buying an RTX 3080. Nope definitely not that. 

SETUP:
- If using Chrome:
  - Download ChromeDriver from https://chromedriver.chromium.org/downloads and add the .exe path to the settings.json file
- If using FireFox:
  - Download GeckoDriver from here: https://github.com/mozilla/geckodriver/releases  and add it to your PATH environment variables.
- Add your information to the 'settings.json' file.
- To Run: 'py app.py' in command line

If you want to use this bot and have it text you when it gets a hit. You will need to make a developer account on Twilio and add your private keys to the mssage.py class.
Like this:
CLIENT = Client("Account SID", "Auth Token")
- You can disable messaging in the settings file if you want.

You need to install GeckoDriver from here: https://github.com/mozilla/geckodriver/releases  and add it to your PATH environment variables.
Required Packages (PIP install): Twilio, Selenuim, Colorama, tqdm, and more. Requirements.txt file is coming soon.
