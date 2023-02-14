from interfaces.models.interface_device_model import IResourceModel
import json


class DeviceModel(IResourceModel):

    def __init__(self, uuid=None, name=None, locationId=None, type=None, attributes=None):
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

    def to_SQL(self):
        return """
            CREATE TABLE device (
            uuid VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            locationId INT(6) NOT NULL,
            type VARCHAR(100) NOT NULL,
            attributes JSON NULL DEFAULT NULL);
            """
