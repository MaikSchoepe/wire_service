import pytest

import tests.gql_operations as ops
from tests.sample_areas import get_sample_area
from tests.sample_places import get_new_sample_place, get_place_count, get_sample_place
from wire_service.app import schema


@pytest.mark.asyncio
async def test_create_place():
    place, data = await get_sample_place()

    assert place.items() >= data.items()
    assert get_place_count() > 0


@pytest.mark.asyncio
async def test_get_places():
    await get_new_sample_place()
    result = await ops.execute_gql(ops.GET_PLACES)

    assert get_place_count() == len(result["places"])


@pytest.mark.asyncio
async def test_get_place_by_id():
    place, data = await get_sample_place()
    place_id = place["id"]
    result = await ops.execute_gql(ops.GET_PLACE, args={"id": place_id})

    assert data.items() == result["place"].items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_place():
    result = await schema.execute(
        ops.GET_PLACE,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Place with ID 666 not found"


@pytest.mark.asyncio
async def test_get_place_parent_name():
    place, _ = await get_sample_place()
    area, _ = await get_sample_area()

    result = await ops.execute_gql(ops.GET_PLACE_PARENT_NAME, args={"id": place["id"]})

    assert result["place"]["parentArea"]["name"] == area["name"]
