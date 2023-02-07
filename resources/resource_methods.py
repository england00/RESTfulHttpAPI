import creation_request.resource_creation_request
from interfaces.interface_resource_methods import IRequests
from json import JSONDecodeError
from flask import request, Response


class SingleResource(IRequests):

    def __init__(self, **kwargs):
        self.dataManager = kwargs['data_manager']

    # GET method: obtaining the resource in json format
    def get(self, resource_id):
        try:
            # checking presence of the searched resource inside the DataManager
            if resource_id in self.dataManager.device_dictionary:
                return self.dataManager.device_dictionary[resource_id].__dict__, 200  # return data and 200 OK code
            else:
                return {'ERROR': "Device Not Found!"}, 404

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # PUT method: updating the resource in json format
    def put(self, resource_id):
        try:
            # the boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)
            resource_creation_request = creation_request.resource_creation_request.IResourceCreationRequest(**json_data)
            creation_request.resource_creation_request.modifyIResourceCreationRequest()

            # finding resource identifier
            check_id = list(list(self.dataManager.device_dictionary.values())[0].__dict__.keys())[0]

            # checking presence of the searched resource inside the DataManager
            if resource_id in self.dataManager.device_dictionary:
                if resource_creation_request.__getattribute__(check_id) != resource_id:
                    return {'ERROR': "UUID mismatch between body and resource"}, 400
                else:
                    update_resource = creation_request.resource_creation_request.IResourceCreationRequest. \
                        from_creation_dto(resource_creation_request)
                    self.dataManager.update_device(update_resource)
                    return Response(status=201, headers={"Location": request.url})
            else:
                return {'ERROR': "Device UUID not found"}, 404

        except JSONDecodeError:
            return {'ERROR': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # DELETE method: removing the resource from the DataManager
    def delete(self, resource_id):
        try:
            # checking presence of the searched resource inside the DataManager
            if resource_id in self.dataManager.device_dictionary:
                self.dataManager.remove_device(resource_id)
                return Response(status=204, headers={"Location": request.url})
            else:
                return {'ERROR': "Device UUID not found"}, 404

        except JSONDecodeError:
            return {'error': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
