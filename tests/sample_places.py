from typing import List, Tuple

import tests.gql_operations as ops
from tests.sample_areas import get_sample_area

_place_data: List[dict] = []

_places: List[dict] = []


async def get_new_place_data() -> dict:
    area, _ = await get_sample_area()
    count = len(_place_data)
    new_data = {
        "areaId": area["id"],
        "shortName": f"TP{count}",
        "name": f"Test Place {count}",
        "description": f"This is sample place number {count}",
    }
    _place_data.append(new_data)
    return new_data


async def get_new_sample_place() -> Tuple[dict, dict]:
    result = await ops.execute_gql(ops.CREATE_PLACE, await get_new_place_data())
    _places.append(result["addPlace"])
    return _places[-1], _place_data[-1]


async def get_sample_place() -> Tuple[dict, dict]:
    if _places:
        return _places[-1], _place_data[-1]
    else:
        return await get_new_sample_place()


def get_place_count() -> int:
    return len(_places)
