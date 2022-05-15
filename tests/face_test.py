import pytest

from tests.place_test import _TestPlaceHandler
from wire_service.app import schema

CREATE_FACE = """
    mutation CreateTestFace(
            $placeId: ID!,
            $orderIndex: Int!,
            $shortName: String!,
            $name: String!,
            $height: Int!,
            $width: Int!,
            $description: String!
        ) {
        addFace(placeId: $placeId, newFace: {
                orderIndex: $orderIndex,
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

    async def last_face_data(self) -> dict:
        return {
            "placeId": await self.get_test_place_id(),
            "orderIndex": _TestFaceHandler.face_count,
            "shortName": f"TF{_TestFaceHandler.face_count}",
            "name": f"Test Face {_TestFaceHandler.face_count}",
            "height": _TestFaceHandler.face_count * 100,
            "width": _TestFaceHandler.face_count * 200,
            "description": f"This is sample face number {_TestFaceHandler.face_count}",
        }

    async def create_face(self) -> dict:
        _TestFaceHandler.face_count += 1
        result = await self._execute(CREATE_FACE, await self.last_face_data())
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

    last_data = (await TestFaceHandler.last_face_data()).items()
    assert last_data <= result.items()  # all sent data is there (exclude the id)


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

    assert sent_data.items() <= result.items()


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
