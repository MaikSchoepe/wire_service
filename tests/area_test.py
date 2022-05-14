import pytest

from wire_service.app import schema

CREATE_AREA = """
    mutation CreateTestArea($shortName: String!, $name: String!, $description: String!) {
        addArea(newArea: {shortName: $shortName, name: $name, description: $description}) {
            id,
            shortName,
            name,
            description
        }
    }
"""

GET_AREAS = """
    { areas {
        id
    }}
"""

GET_AREA = """
    query GetArea($id: ID!) {
        area(id: $id) {
            name,
            shortName,
            description
        }
    }
"""


class _TestAreaHandler:
    area_count = 0

    @property
    def last_area_data(self) -> dict:
        return {
            "shortName": f"TA{_TestAreaHandler.area_count}",
            "name": f"Test Area {_TestAreaHandler.area_count}",
            "description": f"This is sample area number {_TestAreaHandler.area_count}",
        }

    async def _execute(self, query: str, args: dict = {}) -> dict:
        result = await schema.execute(
            query,
            variable_values=args,
        )
        assert result.errors is None
        assert isinstance(result.data, dict)
        return result.data

    async def create_area(self) -> dict:
        _TestAreaHandler.area_count += 1
        return (await self._execute(CREATE_AREA, self.last_area_data))["addArea"]

    async def get_areas(self) -> dict:
        return (await self._execute(GET_AREAS))["areas"]

    async def get_area(self, **kwargs) -> dict:
        return (await self._execute(GET_AREA, kwargs))["area"]


TestAreaHandler = _TestAreaHandler()


@pytest.mark.asyncio
async def test_create_area():
    result = await TestAreaHandler.create_area()

    assert TestAreaHandler.last_area_data.items() <= result.items()


@pytest.mark.asyncio
async def test_get_areas():
    await TestAreaHandler.create_area()

    result = await TestAreaHandler.get_areas()
    assert len(result) == TestAreaHandler.area_count


@pytest.mark.asyncio
async def test_get_area_by_id():
    result = await TestAreaHandler.create_area()
    sent_data = TestAreaHandler.last_area_data

    area_id = result["id"]

    result = await TestAreaHandler.get_area(id=area_id)

    assert sent_data.items() <= result.items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_area():
    result = await schema.execute(
        GET_AREA,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Area with ID 666 not found"
