import tests.gql_operations as ops
from tests.sample_places import get_sample_place

_face_data: list[dict] = []

_faces: list[dict] = []


async def get_new_face_data(add_last: bool = True) -> dict:
    place, _ = await get_sample_place()
    count = len(_face_data)
    new_data = {
        "placeId": place["id"],
        "addLast": add_last,
        "shortName": f"TF{count}",
        "name": f"Test Face {count}",
        "height": count * 100 + 10,
        "width": count * 200 + 20,
        "description": f"This is sample face number {count}",
    }
    _face_data.append(new_data)
    return new_data


async def get_new_sample_face(add_last: bool = True) -> tuple[dict, dict]:
    result = await ops.execute_gql(ops.CREATE_FACE, await get_new_face_data(add_last))
    _faces.append(result["addFace"])
    return _faces[-1], _face_data[-1]


async def get_sample_face() -> tuple[dict, dict]:
    if _faces:
        return _faces[-1], _face_data[-1]
    else:
        return await get_new_sample_face()


def get_face_count() -> int:
    return len(_faces)
