import enum

import strawberry


@strawberry.enum
class CableKind(enum.Enum):
    POWER = "power"
    DATA = "data"
