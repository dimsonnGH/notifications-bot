
import os
import sys
import requests
import logging
import telegram

def print_2_log(message_text, *args):

  global error_counter
  error_counter += 1

  logging.error(message_text.format(*args))

TIMEOUT = 120
MAX_ERROR_COUNT = 5
DVMN_TOKEN = os.getenv("DVNM_BOT_DVMN_TOKEN")
TELEGRAM_TOKEN = os.getenv("DVNM_BOT_TELEGRAM_TOKEN")
CHAT_ID = os.getenv("DVNM_BOT_CHAT_ID")

url = 'https://dvmn.org/api/long_polling/'
headers = {"Authorization":"Token " + DVMN_TOKEN}

bot = telegram.Bot(token = TELEGRAM_TOKEN)

#logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s', filename = 'error_log.log')
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s', stream = sys.stdout, level=logging.INFO)
logging.info('bot started')

timestamp = 0
params = {}
error_counter = 0

while error_counter <= MAX_ERROR_COUNT:

  if timestamp:
    params = {'timestamp' : str(timestamp)}

  try:

    response = requests.get(url, headers = headers, timeout = TIMEOUT, params = params)
    response.raise_for_status()

  except requests.exceptions.ReadTimeout:

    print_2_log('Request timeout. URL: {}', response.url)

  except requests.exceptions.ConnectionError:

    print_2_log('Connection error.')

  except requests.exceptions.HTTPError:

    print_2_log('HTTP error. Status code: {}. URL: {}', response.status_code, response.url)

  else:

    error_counter = 0

    as_json = response.json()
    if not 'status' in as_json:
      continue

    response_status = as_json['status']

    if response_status == 'TIMEOUT':
      
      timestamp = as_json['timestamp_to_request']
      continue

    if response_status == 'found':

      timestamp = as_json['last_attempt_timestamp']

      for lesson in as_json['new_attempts']:

        message_text = 'У вас проверили работу «{0}»'.format(lesson['lesson_title'])
          
        bot.send_message(chat_id = CHAT_ID, text = message_text)
        
        if lesson['is_negative']:
          message_text = 'К сожалению, в работе нашлись ошибки.'
        else:
          message_text = 'Преподавателю все понравилось, можно приступать к слеюдующему уроку!'

        bot.send_message(chat_id = CHAT_ID, text = message_text)


