import pytest

from tests.area_test import _TestAreaHandler
from wire_service.app import schema

CREATE_PLACE = """
    mutation CreateTestPlace($areaId: ID!, $shortName: String!, $name: String!, $description: String!) {
        addPlace(areaId: $areaId, newPlace: {shortName: $shortName, name: $name, description: $description}) {
            areaId,
            id,
            shortName,
            name,
            description
        }
    }
"""

GET_PLACES = """
    { places {
        id
    }}
"""

GET_PLACE = """
    query GetPlace($id: ID!) {
        place(id: $id) {
            areaId,
            name,
            shortName,
            description
        }
    }
"""

GET_PLACE_PARENT_NAME = """
    query GetPlace($id: ID!) {
        place(id: $id) {
            parentArea {
                name
            }
        }
    }
"""


class _TestPlaceHandler(_TestAreaHandler):
    place_count = 0

    def __init__(self) -> None:
        self._area_id = None
        self.place_parent_name = None

    async def get_test_area_id(self):
        if not self._area_id:
            result = await self.create_area()
            self._area_id = result["id"]
            self.place_parent_name = result["name"]
        return self._area_id

    async def last_place_data(self) -> dict:
        return {
            "areaId": await self.get_test_area_id(),
            "shortName": f"TP{self.place_count}",
            "name": f"Test Place {self.place_count}",
            "description": f"This is sample place number {self.place_count}",
        }

    async def create_place(self) -> dict:
        self.place_count += 1
        result = await self._execute(CREATE_PLACE, await self.last_place_data())
        return result["addPlace"]

    async def get_place(self, **kwargs) -> dict:
        return (await self._execute(GET_PLACE, kwargs))["place"]

    async def get_places(self) -> dict:
        return (await self._execute(GET_PLACES))["places"]

    async def get_place_parent_id(self, **kwargs) -> dict:
        data = await self._execute(GET_PLACE_PARENT_NAME, kwargs)
        return data["place"]["parentArea"]["name"]


TestPlaceHandler = _TestPlaceHandler()


@pytest.mark.asyncio
async def test_create_place():
    result = await TestPlaceHandler.create_place()

    last_data = (await TestPlaceHandler.last_place_data()).items()
    assert last_data <= result.items()  # all sent data is there (exclude the id)


@pytest.mark.asyncio
async def test_get_places():
    await TestPlaceHandler.create_place()

    result = await TestPlaceHandler.get_places()
    assert len(result) == TestPlaceHandler.place_count


@pytest.mark.asyncio
async def test_get_place_by_id():
    result = await TestPlaceHandler.create_place()
    sent_data = await TestPlaceHandler.last_place_data()

    place_id = result["id"]

    result = await TestPlaceHandler.get_place(id=place_id)

    assert sent_data.items() <= result.items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_place():
    result = await schema.execute(
        GET_PLACE,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Place with ID 666 not found"


@pytest.mark.asyncio
async def test_get_place_parent_name():
    result = await TestPlaceHandler.create_place()

    parent_name = TestPlaceHandler.place_parent_name
    place_id = result["id"]
    assert parent_name
    assert place_id

    result = await TestPlaceHandler.get_place_parent_id(id=place_id)

    assert result == parent_name
