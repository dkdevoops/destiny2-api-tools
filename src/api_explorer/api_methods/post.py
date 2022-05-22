import typing as t
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError

from .models import *
from .common import *
from .factory import url_builder


async def post_request(url: str) -> t.Union[GenericApiResponse, None]:
    try:
        async with ClientSession() as session:
            async with session.get(url, headers=HEADERS) as r:
                json_res = await r.json()
                data = GenericApiResponse.parse_obj(json_res)
                return data
    except ClientResponseError as e:
        print(e)
        return None


async def refresh_token():
    refresh_url = 'https://www.bungie.net/platform/app/oauth/token/'


