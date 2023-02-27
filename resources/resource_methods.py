from creation_request.resource_creation_request import IResourceCreationRequest
from interfaces.resources.interface_resource_methods import IRequests
from json import JSONDecodeError
from flask import request, Response


class SingleResource(IRequests):

    def __init__(self, **kwargs):
        self.resources_mapper = kwargs['resources_mapper']
        self.endpoint = kwargs['endpoint']

    # GET method: obtaining the resource in json format
    def get(self, resource_id):
        try:
            # checking presence of the searched resource inside the ResourcesMapper
            for resource in self.resources_mapper.get_resources().values():
                if request.url.split(self.endpoint)[1] == resource.get_uri() or\
                        request.url.split(self.endpoint)[1] == '/' + resource.get_uri():
                    return resource.__dict__, 200  # return data and 200 OK code
            return {'ERROR': "Resource Not Found!"}, 404

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # PUT method: updating the resource in json format
    def put(self, resource_id):
        try:
            try:
                # the boolean flag force the parsing of PUT data as JSON irrespective of the mimetype
                json_data = request.get_json(force=True)
                resource_creation_request = IResourceCreationRequest(json_data)

                # checking if the searched resource is already present inside the ResourcesMapper
                if resource_creation_request.get_uuid() in self.resources_mapper.get_resources().keys():
                    # checking if the searched resource has the url's path inside her attribute 'uri'
                    if request.url.split(self.endpoint)[1] != resource_creation_request.get_uri() and\
                            request.url.split(self.endpoint)[1] != '/' + resource_creation_request.get_uri():
                        return {'ERROR': "URI mismatch between body and resource"}, 400
                    else:
                        self.resources_mapper.update_resource(resource_creation_request)
                        return Response(status=201, headers={"Location": request.url})
                else:
                    return {'ERROR': "Resource UUID not found"}, 404

            except JSONDecodeError:
                return {'ERROR': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # DELETE method: removing the resource from the ResourcesMapper
    def delete(self, resource_id):
        try:
            try:
                # checking presence of the searched resource inside the ResourcesMapper
                for resource in self.resources_mapper.get_resources().values():
                    # checking if the searched resource has the url's path inside her attribute 'uri'
                    if request.url.split(self.endpoint)[1] == resource.get_uri() or \
                            request.url.split(self.endpoint)[1] == '/' + resource.get_uri():
                        self.resources_mapper.remove_resource(resource.get_uuid())
                        return Response(status=204, headers={"Location": request.url})
                return {'ERROR': "Resource Not Found!"}, 404

            except JSONDecodeError:
                return {'ERROR': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
