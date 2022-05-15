import pytest

from tests.place_test import _TestPlaceHandler
from wire_service.app import schema

CREATE_FACE = """
    mutation CreateTestFace(
            $placeId: ID!,
            $addLast: Boolean!,
            $shortName: String!,
            $name: String!,
            $height: Int!,
            $width: Int!,
            $description: String!
        ) {
        addFace(placeId: $placeId, addLast: $addLast, newFace: {
                shortName: $shortName,
                name: $name,
                height: $height,
                width: $width,
                description: $description
            }) {
                placeId,
                id,
                orderIndex,
                shortName,
                height,
                width,
                name,
                description,
            }
    }
"""

GET_FACES = """
    { faces {
        id
    }}
"""

GET_FACE = """
    query GetFace($id: ID!) {
        face(id: $id) {
            placeId,
            orderIndex,
            name,
            shortName,
            height,
            width,
            description
        }
    }
"""

GET_FACE_PARENT_NAME = """
    query GetFace($id: ID!) {
        face(id: $id) {
            parentPlace {
                name
            }
        }
    }
"""

IGNORED_KEYS = ["addLast", "orderIndex", "id"]


def dict_equals(d1, d2):
    return sorted([(k, v) for k, v in d1.items() if k not in IGNORED_KEYS]) == sorted(
        [(k, v) for k, v in d2.items() if k not in IGNORED_KEYS]
    )


class _TestFaceHandler(_TestPlaceHandler):
    face_count = 0

    def __init__(self) -> None:
        super().__init__()
        self._place_id = None
        self.face_parent_name = None

    async def get_test_place_id(self):
        if not self._place_id:
            result = await self.create_place()
            self._place_id = result["id"]
            self.face_parent_name = result["name"]
        return self._place_id

    async def last_face_data(self, add_last=True) -> dict:
        return {
            "placeId": await self.get_test_place_id(),
            "addLast": add_last,
            "shortName": f"TF{_TestFaceHandler.face_count}",
            "name": f"Test Face {_TestFaceHandler.face_count}",
            "height": _TestFaceHandler.face_count * 100,
            "width": _TestFaceHandler.face_count * 200,
            "description": f"This is sample face number {_TestFaceHandler.face_count}",
        }

    async def create_face(self, add_last=True) -> dict:
        _TestFaceHandler.face_count += 1
        result = await self._execute(CREATE_FACE, await self.last_face_data(add_last))
        return result["addFace"]

    async def get_face(self, **kwargs) -> dict:
        return (await self._execute(GET_FACE, kwargs))["face"]

    async def get_faces(self) -> dict:
        return (await self._execute(GET_FACES))["faces"]

    async def get_face_parent_id(self, **kwargs) -> dict:
        data = await self._execute(GET_FACE_PARENT_NAME, kwargs)
        return data["face"]["parentPlace"]["name"]


TestFaceHandler = _TestFaceHandler()


@pytest.mark.asyncio
async def test_create_face():
    result = await TestFaceHandler.create_face()

    last_data = await TestFaceHandler.last_face_data()
    assert dict_equals(last_data, result)  # all sent data is there (exclude the id)


@pytest.mark.asyncio
async def test_get_faces():
    await TestFaceHandler.create_face()

    result = await TestFaceHandler.get_faces()
    assert len(result) == TestFaceHandler.face_count


@pytest.mark.asyncio
async def test_get_face_by_id():
    result = await TestFaceHandler.create_face()
    sent_data = await TestFaceHandler.last_face_data()

    face_id = result["id"]

    result = await TestFaceHandler.get_face(id=face_id)

    assert dict_equals(sent_data, result)


@pytest.mark.asyncio
async def test_try_get_nonexistent_face():
    result = await schema.execute(
        GET_FACE,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Face with ID 666 not found"


@pytest.mark.asyncio
async def test_get_face_parent_name():
    result = await TestFaceHandler.create_face()

    parent_name = TestFaceHandler.face_parent_name
    face_id = result["id"]
    assert parent_name
    assert face_id

    result = await TestFaceHandler.get_face_parent_id(id=face_id)

    assert result == parent_name


@pytest.mark.asyncio
async def test_face_ordering():
    face1 = await TestFaceHandler.create_face()
    face2 = await TestFaceHandler.create_face(False)
    face3 = await TestFaceHandler.create_face()
    face4 = await TestFaceHandler.create_face(False)

    assert face1["orderIndex"] > face2["orderIndex"]
    assert face3["orderIndex"] > face1["orderIndex"]
    assert face4["orderIndex"] < face2["orderIndex"]
