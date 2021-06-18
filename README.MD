# dvmn-bot 

Telegram-бот для уведомления о проверке работ на [Devman](https://dvmn.org).

## Запуск
Для запуска необходимо:
- Получить токен доступа к [API Devman](https://dvmn.org/api/docs/).
- Зарегистрировать бота в Telegram. Для этого напишите [Отцу ботов](https://telegram.me/BotFather) команду `\start`, а затем `\newbot`. Отец ботов вернет токен доступа к API Telegram.
- Получить свой chat_id. Для этого напишите в Telegram специальному боту: @userinfobot
- Клонировать данный репозиторий:
- Создать файл ```env\.env``` и установить в нем следующие переменные:

```DVNM_BOT_TELEGRAM_TOKEN=<токен доступа к API Telegram>```

```DVNM_BOT_DVMN_TOKEN=<токен доступа к API Devman>```

```DVNM_BOT_CHAT_ID=<chat_id>```

- Установить зависимости: 

```
pip install -r requirements.txt
```

- Запустить

```
python main.py
```

