
import os
import sys
import requests
import logging
import telegram

print("hello world")

#logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s', filename = 'error_log.log', level=logging.DEBUG)
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s', stream = sys.stdout)

logging.info('start bot')


TIMEOUT = 120
MAX_ERROR_COUNT = 5
DVMN_TOKEN = os.getenv("DVNM_BOT_DVMN_TOKEN")
TELEGRAM_TOKEN = os.getenv("DVNM_BOT_TELEGRAM_TOKEN")
CHAT_ID = os.getenv("DVNM_BOT_CHAT_ID")

url = 'https://dvmn.org/api/long_polling/'
headers = {"Authorization":"Token " + DVMN_TOKEN}

bot = telegram.Bot(token = TELEGRAM_TOKEN)

message_text = 'start bot'
          
bot.send_message(chat_id = CHAT_ID, text = message_text)


