import tests.gql_operations as ops
from tests.sample_faces import get_sample_face

_outlet_data: list[dict] = []

_outlets: list[dict] = []


async def get_new_outlet_data() -> dict:
    face, _ = await get_sample_face()
    count = len(_outlet_data)
    new_data = {
        "faceId": face["id"],
        "shortName": f"TO{count}",
        "name": f"Test Outlet {count}",
        "description": f"This is sample outlet number {count}",
        "kind": "SINGLE",
    }
    _outlet_data.append(new_data)
    return new_data


async def get_new_sample_outlet() -> tuple[dict, dict]:
    result = await ops.execute_gql(ops.CREATE_OUTLET, await get_new_outlet_data())
    _outlets.append(result["addOutlet"])
    return _outlets[-1], _outlet_data[-1]


async def get_sample_outlet() -> tuple[dict, dict]:
    if _outlets:
        return _outlets[-1], _outlet_data[-1]
    else:
        return await get_new_sample_outlet()


def get_outlet_count() -> int:
    return len(_outlets)
