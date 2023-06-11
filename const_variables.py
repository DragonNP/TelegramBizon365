import logging
import os

PATH_TO_USERS_DATA_BASE = './data/users.json'
PATH_TO_WEBINARS_DATA_BASE = './data/webinars.json'
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_API', None)
GLOBAL_LOGGER_LEVEL = os.environ.get('LOGGER_LEVEL', logging.INFO)
