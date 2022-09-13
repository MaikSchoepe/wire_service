import pytest

import tests.gql_operations as ops
from tests.sample_areas import get_area_count, get_new_sample_area, get_sample_area
from wire_service.app import schema


@pytest.mark.asyncio
async def test_create_area():
    area, data = await get_sample_area()

    assert area.items() >= data.items()
    assert get_area_count() > 0


@pytest.mark.asyncio
async def test_get_areas():
    await get_new_sample_area()
    result = await ops.execute_gql(ops.GET_AREAS)

    assert get_area_count() == len(result["areas"])


@pytest.mark.asyncio
async def test_get_area_by_id():
    area, data = await get_sample_area()
    area_id = area["id"]
    result = await ops.execute_gql(ops.GET_AREA, args={"id": area_id})

    assert data.items() == result["area"].items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_area():
    result = await schema.execute(
        ops.GET_AREA,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Area with ID 666 not found"
