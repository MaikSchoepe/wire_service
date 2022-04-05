import pytest

from wire_service.app import schema

CREATE_AREA = """
    mutation CreateTestArea($shortName: String!, $name: String!, $description: String!) {
        addArea(shortName: $shortName, name: $name, description: $description) {
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


class _TestAreaCreator:
    def __init__(self) -> None:
        self.area_count = 0

    def get_last_test_data(self) -> dict:
        return {
            "shortName": f"TA{self.area_count}",
            "name": f"Test Area {self.area_count}",
            "description": f"This is sample area number {self.area_count}",
        }

    def create_area(self):
        self.area_count += 1
        return schema.execute(
            CREATE_AREA,
            variable_values=self.get_last_test_data(),
        )


TestAreaCreator = _TestAreaCreator()


@pytest.mark.asyncio
async def test_create_area():
    result = await TestAreaCreator.create_area()

    assert result.errors is None
    assert result.data["addArea"] == TestAreaCreator.get_last_test_data()


@pytest.mark.asyncio
async def test_get_areas():
    result = await TestAreaCreator.create_area()

    assert result.errors is None

    result = await schema.execute(GET_AREAS)
    assert result.errors is None
    assert len(result.data["areas"]) == TestAreaCreator.area_count
