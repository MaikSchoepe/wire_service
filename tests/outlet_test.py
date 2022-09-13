import pytest

import tests.gql_operations as ops
from tests.sample_faces import get_sample_face
from tests.sample_outlet import (
    get_new_sample_outlet,
    get_outlet_count,
    get_sample_outlet,
)
from wire_service.app import schema


@pytest.mark.asyncio
async def test_create_outlet():
    outlet, data = await get_sample_outlet()

    assert outlet.items() >= data.items()
    assert get_outlet_count() > 0


@pytest.mark.asyncio
async def test_get_outlets():
    await get_new_sample_outlet()
    result = await ops.execute_gql(ops.GET_OUTLETS)

    assert get_outlet_count() == len(result["outlets"])


@pytest.mark.asyncio
async def test_get_outlet_by_id():
    outlet, data = await get_sample_outlet()
    outlet_id = outlet["id"]
    result = await ops.execute_gql(ops.GET_OUTLET, args={"id": outlet_id})

    assert data.items() <= result["outlet"].items()


@pytest.mark.asyncio
async def test_try_get_nonexistent_outlet():
    result = await schema.execute(
        ops.GET_OUTLET,
        variable_values={"id": 666},
    )

    assert result.errors[0].message == "Outlet with ID 666 not found"


@pytest.mark.asyncio
async def test_get_outlet_parent_name():
    outlet, _ = await get_sample_outlet()
    face, _ = await get_sample_face()

    result = await ops.execute_gql(
        ops.GET_OUTLET_PARENT_NAME, args={"id": outlet["id"]}
    )

    assert result["outlet"]["parentFace"]["name"] == face["name"]
