import pytest

import tests.gql_operations as ops
from wire_service.settings import load_cable_types


@pytest.mark.asyncio
async def test_get_cable_types():
    result = await ops.execute_gql(ops.GET_CABLE_TYPES)
    cable_types_config = load_cable_types()

    assert len(cable_types_config) == len(result["cableTypes"])
