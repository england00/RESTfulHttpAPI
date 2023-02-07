import creation_request.resource_creation_request
from interfaces.interface_resources_methods import IRequests
from flask_restful import reqparse
from json import JSONDecodeError
from flask import request, Response


class Resources(IRequests):

    def __init__(self, **kwargs):
        self.dataManager = kwargs['data_manager']

    # GET method: obtaining the list in json format of all the resource which respect the query
    def get(self):
        try:
            # finding resource arguments
            resources_args = list(list(self.dataManager.device_dictionary.values())[0].__dict__.keys())

            # checking query arguments
            parser = reqparse.RequestParser()
            for arg in resources_args:
                parser.add_argument(arg, location='args')

            # creating filters
            filters = []
            args = parser.parse_args()
            for arg in resources_args:
                filters.append(args[arg])

            # checking the number of arguments inside the query
            a = []
            for i in range(len(filters)):
                if filters[i] is not None:
                    a.append(resources_args[i])
            resources_args = a

            # iterate over the dictionary to build a serializable resource list
            resource_list = []
            for resource in self.dataManager.device_dictionary.values():
                if len(resources_args) != 0:  # checking arguments number inside the query
                    past_checks = 0
                    for arg in resources_args:
                        if resource.__getattribute__(arg) == args[arg]:
                            past_checks += 1
                    if past_checks == len(resources_args):
                        resource_list.append(resource.__dict__)  # adding only elements which respect the query
                else:
                    resource_list.append(resource.__dict__)  # adding all the elements if there is no query

            # checking not having an empty list
            if len(resource_list) != 0:
                return resource_list, 200  # return data and 200 OK code
            return {'ERROR': "Resources Not Found!"}, 404

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # POST method: adding a resource and saving it in json format inside the resource list
    def post(self):
        try:
            # the boolean flag force the parsing of POST data as JSON irrespective of the mimetype
            json_data = request.get_json(force=True)
            resource_creation_request = creation_request.resource_creation_request.IResourceCreationRequest(**json_data)
            creation_request.resource_creation_request.modifyIResourceCreationRequest()

            # finding resource identifier
            resource_id = list(list(self.dataManager.device_dictionary.values())[0].__dict__.keys())[0]

            # checking if the searched resource is already present inside the DataManager
            if resource_creation_request.__getattribute__(resource_id) in self.dataManager.device_dictionary:
                return {'ERROR': "Resource already exists"}, 409
            else:
                new_resource = creation_request.resource_creation_request.IResourceCreationRequest.\
                    from_creation_dto(resource_creation_request)
                self.dataManager.add_device(new_resource)
                return Response(status=201, headers={
                    "Location": request.url + "/" + new_resource.__getattribute__(resource_id)})

        except JSONDecodeError:
            return {'ERROR': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
