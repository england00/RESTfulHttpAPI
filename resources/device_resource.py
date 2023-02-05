from json import JSONDecodeError
from flask import request, Response
from flask_restful import Resource
from dto.device_creation_request import DeviceCreationRequest


class DeviceResource(Resource):

    def __init__(self, **kwargs):
        self.dataManager = kwargs['data_manager']

    def get(self, device_id):
        # in this method we can obtain the list of all the specs of a single device only from the device id
        if device_id in self.dataManager.device_dictionary:
            return self.dataManager.device_dictionary[device_id].__dict__, 200  # return data and 200 OK code
        else:
            return {'ERROR': "Device Not Found!"}, 404

    def put(self, device_id):
        # in this method we can update the specs of different devices together controlling information in json format
        try:
            if device_id in self.dataManager.device_dictionary:
                # The boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                json_data = request.get_json(force=True)
                device_creation_request = DeviceCreationRequest(**json_data)
                if device_creation_request.uuid != device_id:
                    return {'ERROR': "UUID mismatch between body and resource"}, 400
                else:
                    self.dataManager.update_device(device_creation_request)
                    return Response(status=201, headers={"Location": request.url + "/" + device_creation_request.uuid})
            else:
                return {'ERROR': "Device UUID not found"}, 404
        except JSONDecodeError:
            return {'ERROR': "Invalid JSON! Check the request"}, 400
        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    def delete(self, device_id):
        # in this method we can directly delete from the list of all the devices a single one only with the device id
        try:
            if device_id in self.dataManager.device_dictionary:
                self.dataManager.remove_device(device_id)
                return Response(status=204, headers={"Location": request.url + "/" + device_id})
            else:
                return {'ERROR': "Device UUID not found"}, 404
        except JSONDecodeError:
            return {'error': "Invalid JSON! Check the request"}, 400
        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
