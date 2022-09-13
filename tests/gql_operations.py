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
