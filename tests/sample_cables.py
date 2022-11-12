import tests.gql_operations as ops
from tests.sample_outlet import get_new_sample_outlet

_cable_data: list[dict] = []

_cables: list[dict] = []


async def get_new_cable_data() -> dict:
    result = await ops.execute_gql(ops.GET_CABLE_TYPES)
    cable_type = result["cableTypes"][0]
    start_outlet, _ = await get_new_sample_outlet()
    end_outlet, _ = await get_new_sample_outlet()
    new_data = {
        "cableTypeId": cable_type["id"],
        "startOutletId": start_outlet["id"],
        "endOutletId": end_outlet["id"],
    }
    _cable_data.append(new_data)
    return new_data


async def get_new_sample_cable() -> tuple[dict, dict]:
    result = await ops.execute_gql(ops.CREATE_CABLE, await get_new_cable_data())
    _cables.append(result["addCable"])
    return _cables[-1], _cable_data[-1]


async def get_sample_cable() -> tuple[dict, dict]:
    if _cables:
        return _cables[-1], _cable_data[-1]
    else:
        return await get_new_sample_cable()


def get_cable_count() -> int:
    return len(_cables)
