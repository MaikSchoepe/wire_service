from wire_service.app import schema


async def execute_gql(query: str, args: dict = {}) -> dict:
    result = await schema.execute(
        query,
        variable_values=args,
    )
    assert result.errors is None
    assert isinstance(result.data, dict)
    return result.data


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

GET_PLACES_OF_AREA = """
    query GetPlacesOfArea($id: ID!) {
        area(id: $id) {
            places {
                id
            }
        }
    }
"""


CREATE_FACE = """
    mutation CreateTestFace(
            $placeId: ID!,
            $addLast: Boolean!,
            $shortName: String!,
            $name: String!,
            $height: Int!,
            $width: Int!,
            $description: String!
        ) {
        addFace(placeId: $placeId, addLast: $addLast, newFace: {
                shortName: $shortName,
                name: $name,
                height: $height,
                width: $width,
                description: $description
            }) {
                placeId,
                id,
                orderIndex,
                shortName,
                height,
                width,
                name,
                description,
            }
    }
"""

GET_FACES = """
    { faces {
        id
    }}
"""

GET_FACE = """
    query GetFace($id: ID!) {
        face(id: $id) {
            placeId,
            orderIndex,
            name,
            shortName,
            height,
            width,
            description
        }
    }
"""

GET_FACE_PARENT_NAME = """
    query GetFace($id: ID!) {
        face(id: $id) {
            parentPlace {
                name
            }
        }
    }
"""

CREATE_OUTLET = """
    mutation CreateTestOutlet(
            $faceId: ID!,
            $shortName: String!,
            $name: String!,
            $description: String!,
            $kind: OutletKind!
        ) {
        addOutlet(faceId: $faceId, newOutlet: {
                shortName: $shortName,
                name: $name,
                description: $description,
                kind: $kind
            }) {
                faceId,
                id,
                name,
                shortName,
                description,
                kind
            }
    }
"""

GET_OUTLETS = """
    { outlets {
        id
    }}
"""

GET_OUTLET = """
    query GetOutlet($id: ID!) {
        outlet(id: $id) {
            faceId,
            name,
            shortName,
            description,
            kind
        }
    }
"""

GET_OUTLET_PARENT_NAME = """
    query GetOutlet($id: ID!) {
        outlet(id: $id) {
            parentFace {
                name
            }
        }
    }
"""

GET_CABLE_TYPES = """
    { cableTypes {
        id,
        name,
        description,
        wires {
            name,
            color,
            secondColor
        }
    }}
"""

CREATE_CABLE = """
    mutation CreateTestCable(
            $cableTypeId: ID!,
            $startOutletId: ID!,
            $endOutletId: ID!,
        ) {
        addCable(cableTypeId: $cableTypeId,
                 startOutletId: $startOutletId,
                 endOutletId: $endOutletId) {
                id,
                cableTypeId,
                startOutletId,
                endOutletId
            }
    }
"""

GET_CABLES = """
    { cables {
        id
    }}
"""

GET_CABLE = """
    query GetCable($id: ID!) {
        cable(id: $id) {
            cableTypeId,
            startOutletId,
            endOutletId
        }
    }
"""
