import pytest

import tests.gql_operations as ops
from tests.sample_faces import get_face_count, get_new_sample_face, get_sample_face
from tests.sample_places import get_sample_place
from wire_service.app import schema

IGNORED_KEYS = ["addLast", "orderIndex", "id"]


def dict_equals(d1, d2):
    return sorted([(k, v) for k, v in d1.items() if k not in IGNORED_KEYS]) == sorted(
        [(k, v) for k, v in d2.items() if k not in IGNORED_KEYS]
    )


@pytest.mark.asyncio
async def test_create_face():
    face, data = await get_sample_face()

    assert dict_equals(face, data)
    assert get_face_count() > 0


@pytest.mark.asyncio
async def test_get_faces():
    await get_new_sample_face()
    result = await ops.execute_gql(ops.GET_FACES)

    assert get_face_count() == len(result["faces"])


@pytest.mark.asyncio
async def test_get_face_by_id():
    face, data = await get_sample_face()
    face_id = face["id"]
    result = await ops.execute_gql(ops.GET_FACE, args={"id": face_id})

    assert dict_equals(result["face"], data)


@pytest.mark.asyncio
async def test_try_get_nonexistent_face():
    result = await schema.execute(
        ops.GET_FACE,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Face with ID 666 not found"


@pytest.mark.asyncio
async def test_get_face_parent_name():
    face, _ = await get_sample_face()
    place, _ = await get_sample_place()

    result = await ops.execute_gql(ops.GET_FACE_PARENT_NAME, args={"id": face["id"]})

    assert result["face"]["parentPlace"]["name"] == place["name"]


@pytest.mark.asyncio
async def test_face_ordering():
    face1, _ = await get_new_sample_face()
    face2, _ = await get_new_sample_face(False)
    face3, _ = await get_new_sample_face()
    face4, _ = await get_new_sample_face(False)

    assert face1["orderIndex"] > face2["orderIndex"]
    assert face3["orderIndex"] > face1["orderIndex"]
    assert face4["orderIndex"] < face2["orderIndex"]
