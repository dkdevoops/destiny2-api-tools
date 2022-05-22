import logging
import typing as t

from .common import *

__all__ = ('get_full_url')

logger = logging.getLogger()


def url_handler(url_base: str, *args) -> str:
    if not args:
        return f'{url_base}/'
    return '/'.join([url_base, *args])


def url_builder(request_type: str, *args) -> t.Union[str, None]:
    match request_type:
        case request_type if 'stats' in request_type.lower():
            return url_handler(STATS, *args)
        case 'settings':
            return url_handler(SETTINGS, *args)
        case 'user':
            return url_handler(USER, *args)
        case 'd2':
            return url_handler(DESTINY2, *args)
        case 'armory':
            return url_handler(ARMORY, *args)
        case _:
            return url_handler(BASE, *args)
