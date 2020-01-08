print("hello world")

"""import os
import requests
import logging
import telegram
from dotenv import load_dotenv

def print_2_log(message_text, *args):

  global error_counter
  error_counter += 1

  logging.error(message_text.format(*args))

basedir = os.path.dirname(__file__)
env_path = os.path.join(basedir, 'env', '.env')
load_dotenv(dotenv_path=env_path)

base_url = 'https://dvmn.org/api/user_reviews/'
url = 'https://dvmn.org/api/long_polling/?timestamp=1555411734'
url = 'https://dvmn.org/api/long_polling/?timestamp=0'
url = 'https://dvmn.org/api/long_polling/?timestamp=1568388672.314161'
url = 'https://dvmn.org/api/_long_polling/'"""

'''TIMEOUT = 120
MAX_ERROR_COUNT = 5
DVMN_TOKEN = os.getenv("DVNM_BOT_DVMN_TOKEN")
TELEGRAM_TOKEN = os.getenv("DVNM_BOT_TELEGRAM_TOKEN")
CHAT_ID = os.getenv("DVNM_BOT_CHAT_ID")

headers = {"Authorization":"Token " + DVMN_TOKEN}

bot = telegram.Bot(token = TELEGRAM_TOKEN)'''

#logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s', filename = 'error_log.log')
#logging.basicConfig(format = '%(levelname)-8s [%(asctime)s]  %(message)s')

'''logging.error("bot started")

timestamp = 0
params = {}
error_counter = 0'''

'''while error_counter < MAX_ERROR_COUNT:

  logging.error("error_counter " + str(error_counter))

  error_counter = error_counter + 1'''

  '''if timestamp:
    params = {'timestamp' : str(timestamp)}

  try:
    response = requests.get(url, headers = headers, timeout = TIMEOUT, params = params)
    response.raise_for_status()
  except requests.exceptions.ReadTimeout:
    print_2_log('Request timeout. URL: {}', response.url)
    #logging.error('Request timeout. URL: {}'.format(response.url))
    #error_counter += 1
    #print("ReadTIMEOUT")
    #pass
  except requests.exceptions.ConnectionError:
    print_2_log('Connection error.')
    #logging.error('Connection error.')
    #error_counter += 1
    #print("ConnectionError")
    #pass
  except requests.exceptions.HTTPError:
    print_2_log('HTTP error. Status code: {}. URL: {}',response.status_code,  response.url)
    #logging.error('HTTP error. Status code: {}. URL: {}'.format(response.status_code, response.url))
    #error_counter += 1
    #print("HTTPError")
    #pass
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
          
        #bot.send_message(chat_id = CHAT_ID, text = message_text)
        print(message_text)

        if lesson['is_negative']:
          message_text = 'К сожалению, в работе нашлись ошибки.'
        else:
          message_text = 'Преподавателю все понравилось, можно приступать к слеюдующему уроку!'

        #bot.send_message(chat_id = CHAT_ID, text = message_text)
        print(message_text)'''

  
  #f = False
