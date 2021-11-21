import os

from logging import config as logging_config

# application setup
from logger import LOGGING

DEBUG = bool(os.getenv('DEBUG', True))
APP_PORT = os.getenv('APP_PORT', 8000)

logging_config.dictConfig(LOGGING)

# docs setup
PROJECT_NAME = 'vk.com parser API'
DOCS_URL = '/api/openapi'


# scraping setup
USER_AGENT_MOBILE = 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
USER_AGENT_DESKTOP = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

DESKTOP_HEADERS = {
    'user-agent': USER_AGENT_DESKTOP,
}
MOBILE_HEADERS = {
    'user-agent': USER_AGENT_MOBILE,
}
