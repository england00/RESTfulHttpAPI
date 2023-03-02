from creation_request.resource_creation_request import IResourceCreationRequest
from interfaces.resources.interface_resources_methods import IRequests
from json import JSONDecodeError
from flask import request, Response


class Resources(IRequests):

    def __init__(self, **kwargs):
        self.resources_mapper = kwargs['resources_mapper']
        self.endpoint = kwargs['endpoint']

    # GET method: obtaining the list in json format of all the resource which respect the query
    def get(self):
        try:
            # iterate over the dictionary to build a serializable resource list
            resource_list = []
            for resource in self.resources_mapper.get_resources().values():
                if request.url.split(self.endpoint)[1] in resource.get_uri() or \
                        request.url.split(self.endpoint)[1] in '/' + resource.get_uri():
                    resource_list.append(resource.__dict__)
                elif request.url.endswith(self.endpoint + '/'):
                    resource_list.append(resource.__dict__)

            # checking not having an empty list
            if len(resource_list) != 0:
                return resource_list, 200  # return data and 200 OK code
            return {'ERROR': "Resources Not Found!"}, 404

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # POST method: adding a resource and saving it in json format inside the resource list
    def post(self):
        try:
            try:
                # the boolean flag force the parsing of POST data as JSON irrespective of the mimetype
                json_data = request.get_json(force=True)
                resource_creation_request = IResourceCreationRequest(json_data)

                # checking if the searched resource has the right 'picking_system' attribute value
                if resource_creation_request.get_picking_system() not in self.endpoint:
                    return {'ERROR': "URI mismatch between body and resource"}, 400
                else:
                    # checking if the searched resource is already present inside the ResourcesMapper
                    if resource_creation_request.get_uuid() in self.resources_mapper.get_resources().keys():
                        return {'ERROR': "Resource already exists"}, 409
                    else:
                        # checking if the new resource has the url's path inside her attribute 'uri'
                        if request.url.split(self.endpoint)[1] not in resource_creation_request.get_uri() and \
                                request.url.split(self.endpoint)[1] not in '/' + resource_creation_request.get_uri():
                            return {'ERROR': "URI mismatch between body and resource"}, 400
                        else:
                            if (request.url.split(self.endpoint)[1] + '{}'.format(
                                resource_creation_request.get_uri().replace('{}'.format(
                                    request.url.split(self.endpoint)[1]), ''))) == resource_creation_request.get_uri() or \
                                    (request.url.split(self.endpoint)[1] + '{}'.format(
                                    str('/' + resource_creation_request.get_uri()).replace('{}'.format(
                                    request.url.split(self.endpoint)[1]), ''))) == '/' + resource_creation_request.get_uri():
                                self.resources_mapper.add_resource(resource_creation_request)
                                return Response(status=201, headers={
                                    "Location": request.url + "/" + resource_creation_request.get_uuid()})
                            else:
                                return {'ERROR': "URI mismatch between body and resource"}, 400

            except JSONDecodeError:
                return {'ERROR': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
