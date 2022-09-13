import enum

import strawberry


@strawberry.enum
class OutletKind(enum.Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    QUADRUPLE = "quadruple"
    PLAIN = "plain"
    DISTRIBUTOR = "distributor"
    OTHER = "other"
