import pytest
from strawberry.types import ExecutionResult

from tests.area_test import TestAreaHandler
from wire_service.app import schema

CREATE_PLACE = """
    mutation CreateTestPlace($areaId: ID!, $shortName: String!, $name: String!, $description: String!) {
        addPlace(areaId: $areaId, shortName: $shortName, name: $name, description: $description) {
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


class _TestPlaceHandler:
    def __init__(self) -> None:
        self.place_count = 0
        self._area_id = None

    async def get_test_area_id(self):
        if not self._area_id:
            result = await TestAreaHandler.create_area()
            self._area_id = result.data["addArea"]["id"]
        return self._area_id

    async def get_last_test_data(self) -> dict:
        return {
            "areaId": await self.get_test_area_id(),
            "shortName": f"TP{self.place_count}",
            "name": f"Test Place {self.place_count}",
            "description": f"This is sample place number {self.place_count}",
        }

    def get_last_test_data_sync(self) -> dict:
        return {
            "areaId": self._area_id,
            "shortName": f"TP{self.place_count}",
            "name": f"Test Place {self.place_count}",
            "description": f"This is sample place number {self.place_count}",
        }

    async def create_place(self) -> ExecutionResult:
        self.place_count += 1
        return await schema.execute(
            CREATE_PLACE,
            variable_values=await self.get_last_test_data(),
        )

    async def get_place(self, **kwargs) -> ExecutionResult:
        return await schema.execute(
            GET_PLACE,
            variable_values=kwargs,
        )


TestPlaceHandler = _TestPlaceHandler()


@pytest.mark.asyncio
async def test_create_place():
    result = await TestPlaceHandler.create_place()

    assert result.errors is None
    assert (
        TestPlaceHandler.get_last_test_data_sync().items()
        <= result.data["addPlace"].items()
    )  # all sent data is there (exclude the id)


@pytest.mark.asyncio
async def test_get_places():
    result = await TestPlaceHandler.create_place()

    assert result.errors is None

    result = await schema.execute(GET_PLACES)
    assert result.errors is None
    assert len(result.data["places"]) == TestPlaceHandler.place_count


@pytest.mark.asyncio
async def test_get_place_by_id():
    result = await TestPlaceHandler.create_place()
    sent_data = TestPlaceHandler.get_last_test_data_sync()

    assert result.errors is None

    place_id = result.data["addPlace"]["id"]

    result = await TestPlaceHandler.get_place(id=place_id)

    assert result.errors is None
    assert sent_data.items() <= result.data["place"].items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_place():
    result = await TestPlaceHandler.get_place(id=666)

    assert result.errors[0].message == "Place with ID 666 not found"
