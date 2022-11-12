import pytest

import tests.gql_operations as ops
from tests.sample_cables import get_cable_count, get_new_sample_cable, get_sample_cable
from wire_service.app import schema


@pytest.mark.asyncio
async def test_create_cable():
    cable, data = await get_sample_cable()

    assert cable.items() >= data.items()
    assert get_cable_count() > 0


@pytest.mark.asyncio
async def test_get_cables():
    await get_new_sample_cable()
    result = await ops.execute_gql(ops.GET_CABLES)

    assert get_cable_count() == len(result["cables"])


@pytest.mark.asyncio
async def test_get_cable_by_id():
    cable, data = await get_sample_cable()
    cable_id = cable["id"]
    result = await ops.execute_gql(ops.GET_CABLE, args={"id": cable_id})

    assert data.items() <= result["cable"].items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_cable():
    result = await schema.execute(
        ops.GET_CABLE,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Cable with ID 666 not found"
