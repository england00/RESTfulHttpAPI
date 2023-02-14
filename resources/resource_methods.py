from creation_request.resource_creation_request import IResourceCreationRequest
from interfaces.resources.interface_resource_methods import IRequests
from json import JSONDecodeError
from flask import request, Response


class SingleResource(IRequests):

    def __init__(self, **kwargs):
        self.resources_mapper = kwargs['resources_mapper']

    # GET method: obtaining the resource in json format
    def get(self, resource_id):
        try:
            # checking presence of the searched resource inside the DataManager
            if resource_id in self.resources_mapper.get_resources():
                return self.resources_mapper.get_resource(resource_id).__dict__, 200  # return data and 200 OK code
            else:
                return {'ERROR': "Device Not Found!"}, 404

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # PUT method: updating the resource in json format
    def put(self, resource_id):
        try:
            # the boolean flag force the parsing of PUT data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)
            resource_creation_request = IResourceCreationRequest(json_data)

            # checking presence of the searched resource inside the DataManager
            if resource_id in self.resources_mapper.get_resources():
                if resource_creation_request.get_uuid() != resource_id:
                    return {'ERROR': "UUID mismatch between body and resource"}, 400
                else:
                    self.resources_mapper.update_resource(resource_creation_request)
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
            if resource_id in self.resources_mapper.get_resources():
                self.resources_mapper.remove_resource(resource_id)
                return Response(status=204, headers={"Location": request.url})
            else:
                return {'ERROR': "Device UUID not found"}, 404

        except JSONDecodeError:
            return {'error': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
