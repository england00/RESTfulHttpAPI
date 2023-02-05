from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource, reqparse
from dto.device_creation_request import DeviceCreationRequest
from model.device_model import DeviceModel


class DevicesResource(Resource):

    def __init__(self, **kwargs):
        self.dataManager = kwargs['data_manager']

    def get(self):
        # in this method we can obtain the list in json format of all the devices

        # check for query arguments
        parser = reqparse.RequestParser()
        parser.add_argument('type', location='args')
        parser.add_argument('locationId', location='args')

        # use required=True to force the check for a specific field
        parser.add_argument('locationId', location='args', required=True)
        args = parser.parse_args()
        locationIdFilter = args["locationId"]

        # iterate over the dictionary to build a serializable device list
        device_list = []
        for device in self.dataManager.device_dictionary.values():
            if device.locationId == locationIdFilter:  # adding only the elements which respect the query
                device_list.append(device.__dict__)
        return device_list, 200  # return data and 200 OK code

    def post(self):
        # in this method we can put a device formatting it in json format inside the devices list
        try:
            # the boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)
            device_creation_request = DeviceCreationRequest(**json_data)
            if device_creation_request.uuid in self.dataManager.device_dictionary:
                return {'error': "Device UUID already exists"}, 409
            else:
                new_device_model = DeviceModel.from_creation_dto(device_creation_request)
                self.dataManager.add_device(new_device_model)
                return Response(status=201, headers={"Location": request.url+"/"+ new_device_model.uuid})
        except JSONDecodeError:
            return {'error': "Invalid JSON ! Check the request"}, 400
        except Exception as e:
            return {'error': "Generic Internal Server Error ! Reason: " + str(e)}, 500
