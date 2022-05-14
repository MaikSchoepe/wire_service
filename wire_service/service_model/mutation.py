from strawberry.tools import merge_types

from wire_service.service_model.area import AreaMutation
from wire_service.service_model.place import PlaceMutation

Mutation = merge_types("Mutation", (AreaMutation, PlaceMutation))
