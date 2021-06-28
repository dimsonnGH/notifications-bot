import os
import sys
import requests
import logging
import telegram
from dotenv import load_dotenv


logger = logging.getLogger("Бот логер")


def print_2_log(message_text, *args) :
    global error_counter

    error_counter += 1
    logger.error(message_text.format(*args))


class BotLogsHandler(logging.Handler) :

    def emit(self, record) :
        log_entry = self.format(record)
        bot.send_message(chat_id=CHAT_ID, text=log_entry)


if __name__ == '__main__' :
    base_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(base_dir, 'env\.env')
    load_dotenv(dotenv_path)
    TIMEOUT = 120
    MAX_ERROR_COUNT = 5
    DVMN_TOKEN = os.getenv("DVNM_BOT_DVMN_TOKEN")
    TELEGRAM_TOKEN = os.getenv("DVNM_BOT_TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("DVNM_BOT_CHAT_ID")

    url = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization" : f"Token {DVMN_TOKEN}"}

    timestamp = 0
    params = {}
    error_counter = 0

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    format_log = '%(levelname)-8s [%(asctime)s]  %(message)s'

    bot_handler = BotLogsHandler()
    formatter = logging.Formatter(format_log)
    bot_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(bot_handler)

    logger.info('bot started')

    while error_counter <= MAX_ERROR_COUNT :

        if timestamp :
            params = {'timestamp' : str(timestamp)}

        try :

            response = requests.get(url, headers=headers, timeout=TIMEOUT, params=params)
            response.raise_for_status()

        except requests.exceptions.ReadTimeout :

            print_2_log('Request timeout. URL: {}', response.url)

        except requests.exceptions.ConnectionError :

            print_2_log('Connection error.')

        except requests.exceptions.HTTPError :

            print_2_log('HTTP error. Status code: {}. URL: {}', response.status_code, response.url)

        else :

            try :
                error_counter = 0

                parsed_response = response.json()
                if not 'status' in parsed_response :
                    continue

                response_status = parsed_response['status']

                if response_status == 'timeout' :
                    timestamp = parsed_response['timestamp_to_request']
                    continue

                if response_status == 'found' :

                    timestamp = parsed_response['last_attempt_timestamp']

                    for lesson in parsed_response['new_attempts'] :

                        message_text = 'У вас проверили работу «{0}»'.format(lesson['lesson_title'])

                        bot.send_message(chat_id=CHAT_ID, text=message_text)

                        if lesson['is_negative'] :
                            message_text = 'К сожалению, в работе нашлись ошибки.'
                        else :
                            message_text = 'Преподавателю все понравилось, можно приступать к слеюдующему уроку!'

                        bot.send_message(chat_id=CHAT_ID, text=message_text)
            except Exception as expt:
                print_2_log(str(expt))
