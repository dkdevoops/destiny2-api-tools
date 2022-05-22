import logging
import typing as t
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError
from pathlib import Path
from urllib.parse import urlencode

from api_explorer.models import *
from .common import *
from .factory import url_builder


logger = logging.getLogger()


__all__ = ('get_user_data', 'get_cleaned_user_names', 'get_vendor_info', 
           'get_d2_manifest', 'get_bnet_settings', 'search_destiny_entities',
           'get_historical_stats_definition', 'get_components', 'get_platform_memberships',
           'get_user_inventory', 'get_entity_manifest')



def response_handler(response: GenericApiResponse, target: t.Optional[ScopedApiRespone] = None) -> t.Union[GenericApiResponse, ScopedResponse]:
    """
    If the source request is successful, returns
    :attr:`~.models.GenericApiResponse.Response`, otherwise returns
    the base response object. 

    :param response: Result of a request execution.
    :type response: :class:`~.models.GenericApiResponse`
    :return: Base response object or that object's `Response` attribute.
    :rtype: :class:`~.models.GenericApiResponse`

    """
    if 'Response' not in response:
        return GenericApiResponse.parse_obj(response)

    if not response['Response']:
        return GenericApiResponse.parse_obj(response)
    
    if target is not None:
        return target.parse_obj(response.get('Response'))
    return GenericApiResponse.parse_obj(response)

async def get_request(url: str, target: t.Optional[ScopedApiRespone] = None) -> t.Union[GenericApiResponse, ScopedResponse]:
    """
    Performs an asynchronouse HTTP `GET` request. Uses :module:`aiohttp`
    as the source for creating an awaitable request session.

    :param url: Url to send the request to.
    :type url: str
    :return: A serialized result of the `GET` request's response. 
    :rtype: :class:`~.models.GenericApiResponse` or None

    """
    try:
        async with ClientSession() as session:
            async with session.get(url, headers=HEADERS) as r:
                json_res = await r.json()
                serialized_resp = response_handler(json_res, target)
                return serialized_resp
    except ClientResponseError as e:
        logger.exception(e)
        return None

async def get_historical_stats_definition() -> GenericApiResponse:
    stats_url = url_builder('stats')
    stats_data: GenericApiResponse = await get_request(stats_url)
    return stats_data

async def get_d2_manifest() -> GenericApiResponse:
    manifest_url = url_builder('d2', 'Manifest')
    manifest_data: GenericApiResponse = await get_request(manifest_url)
    return manifest_data

async def get_bnet_settings() -> GenericApiResponse:
    settings_url = url_builder('settings')
    settings_data: GenericApiResponse = await get_request(settings_url)
    return settings_data

async def get_entity_manifest(entity_type: str, hash_id: str) -> GenericApiResponse:
    item_manifest_url = url_builder('d2', 'Manifest', entity_type, hash_id)
    manifest_data: GenericApiResponse = await get_request(item_manifest_url)
    return manifest_data

async def get_user_data(member_id: str) -> UserApiResponse:
    user_url = url_builder('user', 'GetBungieNetUserById', member_id)
    user_data: UserApiResponse = await get_request(user_url, UserApiResponse)
    return user_data

async def get_cleaned_user_names(member_id: str) -> CleanUserNames:
    user_url = url_builder('user', 'GetSanitizedPlatformDisplayNames', member_id)
    user_data: CleanUserNames = await get_request(user_url, CleanUserNames)
    return user_data

async def get_user_inventory(
    member_id: str, 
    to_file: bool = False, 
    file_path: t.Union[str, Path, None] = None
    ) -> t.List[D2Profile]:
    
    user: UserApiResponse = await get_user_data(member_id)
    memberships: PlatformMembership = await get_platform_memberships(user.membership_id)

    inventory = []

    for profile in memberships.profiles:
        profile_inventory = await get_components(profile.membership_id, components=DEFAULT_COMPONENTS)
        if to_file:
            inventory_file_handler(profile.display_name.lower(), profile_inventory, file_path)
        inventory.append(profile_inventory)
    return inventory

async def search_destiny_entities(entity_type: str, search_term: str, page: int = 0) -> GenericApiResponse:
    entity_url = url_builder('armory', 'Search', entity_type, search_term, f'?page={page}')
    entity_data: GenericApiResponse = await get_request(entity_url)
    return entity_data

async def get_platform_memberships(membership_id: str) -> PlatformMembership:
    membership_url = url_builder('d2', f'254/Profile/{membership_id}/LinkedProfiles/?getAllMemberships=true')
    memberships: PlatformMembership = await get_request(membership_url, PlatformMembership)
    return memberships

async def get_components(member_id: str, components: t.List[int]) -> D2Profile:
    # https://bungie-net.github.io/#/components/schemas/Destiny.DestinyComponentType
    user_data = await get_platform_memberships(member_id)

    if not user_data:
        logger.error('Could not retrieve user information')
        return None
    
    if not user_data.profiles:
        logger.error('Could not get user profile information')
        return None

    components_query = urlencode({'components': ','.join([str(c) for c in components])})

    for profile in user_data.profiles:
        component_url = url_builder('d2', '2', 'Profile', profile.membership_id, f'?{components_query}')
        component_data: GenericApiResponse = await get_request(component_url)
    return response_handler(component_data, D2Profile)

def inventory_file_handler(
    profile_name: str, 
    inventory: D2Profile, 
    file_path: t.Union[str, Path, None] = None
    ) -> t.NoReturn:
    
    match file_path:
        case None:
            file_name = f'{profile_name}_inventory.json'
            inventory.to_file(file_name)
            return
        case Path():
            file_name = file_path.joinpath(f'{profile_name}_inventory.json')
            inventory.to_file(file_name)
            return
        case str():
            file_name = Path(file_path).joinpath(f'{profile_name}_inventory.json')
            inventory.to_file(file_name)
            return