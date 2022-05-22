
import asyncio
import logging
import sys
import typing as t
from argparse import ArgumentParser, Namespace
from functools import partial
from pandas import json_normalize


logger = logging.getLogger()

from api_methods import *


async def handle_args(args: t.Union[Namespace, None]) -> t.Callable:
    if getattr(args, 'member_id') is None:
        match args:
            # Do not require member ID
            case args if getattr(args, 'manifest') is not None:
                return await get_d2_manifest()
            case args if (manifest := getattr(args, 'entity_manifest')) is not None and manifest:
                if (entity_type := getattr(args, 'entity_type')) is not None:
                    return await get_entity_manifest(entity_type)
                logger.info('No entity type provided, getting default manifest')
                return await get_d2_manifest()
            case args if (settings := getattr(args, 'settings')) is not None and settings:
                return await get_bnet_settings()
            case args if (stats_definition := getattr(args, 'stats_definition')) is not None and stats_definition:
                return await get_historical_stats_definition()
            case args if (entities := getattr(args, 'entities')) is not None and entities:
                if (search_term := getattr(args, 'search_term')) is None:
                    logger.error('Search term required to search for entities')
                    return None
                if (entity_type := getattr(args, 'entity_type')) is not None:
                    logger.error('Entity type required to search for entities')
                    return None
                page = getattr(args, 'search_page', 0)
                return await search_destiny_entities(entity_type, search_term, page)

    if (member_id := args.member_id) is None:
        logger.error('Member ID required for remaining requests')
        return None
    
    match args:
        # Require member ID
        case user_data if (user_data := getattr(args, 'user_data')) is not None and user_data:
            return await get_user_data(member_id)
        case user_names if (user_names := getattr(args, 'user_names')) is not None and user_names:
            return await get_cleaned_user_names(member_id)
        case memberships if (memberships := getattr(args, 'memberships')) is not None and memberships:
            return await get_platform_memberships(member_id)
        case components if (components := getattr(args, 'components')) is not None and components:
            if not (component_ids := args.component_ids):
                logger.error('Component ID(s) required to search for components')
                return None
            return await get_components(member_id, component_ids)
        case inventory if (inventory := getattr(args, 'inventory')) is not None and inventory:
            return await get_user_inventory(member_id)


def flatten(obj: t.Dict, sep='.'):
    flat_dict = json_normalize(obj, sep=sep).to_dict(orient='records')
    return list(flat_dict)


async def main(args: Namespace):
    response = await handle_args(args)

    match response:
        case dict():
            print(response)
        case list():
            for i in response:
                print(i)
        case _:
            print(response.dict())
    


if __name__ == '__main__':
    parser = ArgumentParser()
    
    # Param switches
    parser.add_argument('--entity-type', type=str)
    parser.add_argument('--search-term', type=str)
    parser.add_argument('--search-page', type=int)
    parser.add_argument('--component-ids', type=int, nargs='+')
    parser.add_argument('--member-id', type=str)

    # Action trigger switches
    parser.add_argument('--user-data', action='store_true')
    parser.add_argument('--user-names', action='store_true')
    parser.add_argument('--entities', action='store_true')
    parser.add_argument('--memberships', action='store_true')
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--manifest', action='store_true')
    parser.add_argument('--settings', action='store_true')
    parser.add_argument('--stats-definition', action='store_true')
    parser.add_argument('--components', action='store_true')
    # parser.add_argument('--vendor-info', action='store_true')
    
    args = parser.parse_args()

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(args))