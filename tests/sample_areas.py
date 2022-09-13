from typing import List, Tuple

import tests.gql_operations as ops

_area_data: List[dict] = []

_areas: List[dict] = []


def get_new_area_data() -> dict:
    count = len(_area_data)
    new_data = {
        "shortName": f"TA{count}",
        "name": f"Test Area {count}",
        "description": f"This is sample area number {count}",
    }
    _area_data.append(new_data)
    return new_data


async def get_new_sample_area() -> Tuple[dict, dict]:
    result = await ops.execute_gql(ops.CREATE_AREA, get_new_area_data())
    _areas.append(result["addArea"])
    return _areas[-1], _area_data[-1]


async def get_sample_area() -> Tuple[dict, dict]:
    if _areas:
        return _areas[-1], _area_data[-1]
    else:
        return await get_new_sample_area()


def get_area_count() -> int:
    return len(_areas)
