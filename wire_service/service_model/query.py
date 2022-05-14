from strawberry.tools import merge_types

from wire_service.service_model.area import AreaQuery
from wire_service.service_model.place import PlaceQuery

Query = merge_types("Query", (AreaQuery, PlaceQuery))
