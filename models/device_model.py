from interfaces.interface_resource_model import IResourceModel
import json


class DeviceModel(IResourceModel):

    def __init__(self, uuid, name, locationId, type, attributes):
        self.uuid = uuid
        self.name = name
        self.locationId = locationId
        self.type = type
        self.attributes = attributes

    @staticmethod
    def from_creation_dto(resource_creation_request):
        return DeviceModel(resource_creation_request.uuid,
                           resource_creation_request.name,
                           resource_creation_request.locationId,
                           resource_creation_request.type,
                           resource_creation_request.attributes)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
