import os
import sys
import requests
import logging
import telegram
import time
from dotenv import load_dotenv

logger = logging.getLogger("Бот логер")


class BotLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(base_dir, 'env\.env')
    load_dotenv(dotenv_path)
    DVMN_TOKEN = os.getenv("DVNM_BOT_DVMN_TOKEN")
    TELEGRAM_TOKEN = os.getenv("DVNM_BOT_TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("DVNM_BOT_CHAT_ID")

    url = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": f"Token {DVMN_TOKEN}"}

    timestamp = 0
    params = {}
    timeout = 120
    connection_error_delay = 300

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    format_log = '%(levelname)-8s [%(asctime)s]  %(message)s'

    bot_handler = BotLogsHandler(bot=bot, chat_id=CHAT_ID)
    formatter = logging.Formatter(format_log)
    bot_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(bot_handler)

    logger.info('Бот запущен')

    while True:

        if timestamp:
            params = {'timestamp': str(timestamp)}

        try:

            response = requests.get(url, headers=headers, timeout=timeout, params=params)
            response.raise_for_status()

        except requests.exceptions.ReadTimeout:

            logger.error('Request timeout. URL: {}'.format(response.url))

        except requests.exceptions.ConnectionError:

            logger.error('Connection error.')
            time.sleep(connection_error_delay)

        except requests.exceptions.HTTPError:

            logger.error('HTTP error. Status code: {}. URL: {}'.format(response.status_code, response.url))

        try:
            parsed_response = response.json()

            response_status = parsed_response['status']

            if response_status == 'timeout':
                timestamp = parsed_response['timestamp_to_request']

            if response_status == 'found':

                timestamp = parsed_response['last_attempt_timestamp']

                for lesson in parsed_response['new_attempts']:

                    message_text = 'У вас проверили работу «{0}»'.format(lesson['lesson_title'])

                    bot.send_message(chat_id=CHAT_ID, text=message_text)

                    if lesson['is_negative']:
                        message_text = 'К сожалению, в работе нашлись ошибки.'
                    else:
                        message_text = 'Преподавателю все понравилось, можно приступать к слеюдующему уроку!'

                    bot.send_message(chat_id=CHAT_ID, text=message_text)

        except Exception as expt:
            logger.exception('Бот сломался')
