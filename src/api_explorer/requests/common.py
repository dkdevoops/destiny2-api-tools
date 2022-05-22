from dotenv import load_dotenv
from os import environ

from ..models import *


load_dotenv()

__all__ = ('client_id', 'HEADERS', 'BASE', 'DESTINY2', 'SETTINGS', 'TOKEN',
           'USER', 'GROUP', 'OAUTH', 'ARMORY', 'STATS', 'DEFAULT_COMPONENTS')

api_key = environ.get('API_KEY')
client_id = environ.get('CLIENT_ID')

HEADERS = {'X-API-KEY': api_key}


"""
Platform URLs
"""
BASE = 'https://www.bungie.net/Platform'
OAUTH='https://www.bungie.net/en/OAuth/Authorize'
DESTINY2 = '/'.join([BASE, 'Destiny2'])
USER = '/'.join([BASE, 'User'])
GROUP = '/'.join([BASE, 'GroupV2'])
ARMORY = '/'.join([BASE, 'Armory'])
STATS = '/'.join([DESTINY2, 'Stats', 'Definition'])
SETTINGS = '/'.join([BASE, 'Settings'])
TOKEN = '/'.join([BASE, 'App', 'OAuth', 'Token'])


"""
Default set of components used when loading a user's
inventory.
"""
DEFAULT_COMPONENTS = [102, 103, 200, 201, 205, 300, 305, 310]