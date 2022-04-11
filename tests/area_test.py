import pytest
from strawberry.types import ExecutionResult

from wire_service.app import schema

CREATE_AREA = """
    mutation CreateTestArea($shortName: String!, $name: String!, $description: String!) {
        addArea(shortName: $shortName, name: $name, description: $description) {
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


class _TestAreaCreator:
    def __init__(self) -> None:
        self.area_count = 0

    def get_last_test_data(self) -> dict:
        return {
            "shortName": f"TA{self.area_count}",
            "name": f"Test Area {self.area_count}",
            "description": f"This is sample area number {self.area_count}",
        }

    async def create_area(self) -> ExecutionResult:
        self.area_count += 1
        return await schema.execute(
            CREATE_AREA,
            variable_values=self.get_last_test_data(),
        )

    async def get_area(self, **kwargs) -> ExecutionResult:
        return await schema.execute(
            GET_AREA,
            variable_values=kwargs,
        )


TestAreaHandler = _TestAreaCreator()


@pytest.mark.asyncio
async def test_create_area():
    result = await TestAreaHandler.create_area()

    assert result.errors is None
    assert (
        TestAreaHandler.get_last_test_data().items() <= result.data["addArea"].items()
    )  # all sent data is there (exclude the id)


@pytest.mark.asyncio
async def test_get_areas():
    result = await TestAreaHandler.create_area()

    assert result.errors is None

    result = await schema.execute(GET_AREAS)
    assert result.errors is None
    assert len(result.data["areas"]) == TestAreaHandler.area_count


@pytest.mark.asyncio
async def test_get_area_by_id():
    result = await TestAreaHandler.create_area()
    sent_data = TestAreaHandler.get_last_test_data()

    assert result.errors is None

    area_id = result.data["addArea"]["id"]

    result = await TestAreaHandler.get_area(id=area_id)

    assert result.errors is None
    assert sent_data.items() <= result.data["area"].items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_area():
    result = await TestAreaHandler.get_area(id=666)

    assert result.errors[0].message == "Area with ID 666 not found"
