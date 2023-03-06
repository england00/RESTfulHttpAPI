from creation_request.resource_creation_request import IResourceCreationRequest
from database.queries.resource_queries import *
from interfaces.resources.interface_resource_methods import IRequests
from json import JSONDecodeError
from flask import request, Response


class SingleResource(IRequests):

    def __init__(self, **kwargs):
        self.endpoint = kwargs['endpoint']
        self.myDB = kwargs['database']

    # GET method: obtaining the resource in json format
    def get(self, resource_id):
        try:
            # checking presence of the searched resource inside MySQL database
            if len(self.myDB.read_query(check_resource("uri", request.url.split(self.endpoint + '/')[1],
                                                       str(self.endpoint).split('/')[
                                                           len(str(self.endpoint).split('/')) - 1]))) != 0:
                resource = from_db_row_to_object(
                    self.myDB.read_query(check_resource("*", request.url.split(self.endpoint + '/')[1],
                                                        str(self.endpoint).split('/')[
                                                            len(str(self.endpoint).split('/')) - 1]))[0])
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
                resource_update_request = IResourceCreationRequest(json_data)

                # checking if the searched resource has the right 'picking_system' attribute value
                if resource_update_request.get_picking_system() not in self.endpoint:
                    return {'ERROR': "URI mismatch between body and resource"}, 400
                else:
                    # checking if the searched resource is already present inside MySQL database
                    for uuid in self.myDB.read_query(
                            showing_resource_table_join_system("uuid",
                                                               str(self.endpoint).split('/')[
                                                                   len(str(self.endpoint).split('/')) - 1])):
                        if resource_update_request.get_uuid() == uuid[0]:
                            # checking if the searched resource has the url's path inside her attribute 'uri'
                            if request.url.split(self.endpoint)[1] != resource_update_request.get_uri() and \
                                    request.url.split(self.endpoint)[1] != '/' + resource_update_request.get_uri():
                                return {'ERROR': "URI mismatch between body and resource"}, 400
                            else:
                                self.myDB.execute_query(modify_row_resource_table(resource_update_request))
                                return Response(status=201, headers={"Location": request.url})
                    else:
                        return {'ERROR': "Resource UUID not found"}, 404

            except JSONDecodeError:
                return {'ERROR': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500

    # DELETE method: removing the resource from MySQL database
    def delete(self, resource_id):
        try:
            try:
                # checking presence of the searched resource inside MySQL database
                for resource in self.myDB.read_query(
                        showing_resource_table_join_system("*",
                                                           str(self.endpoint).split('/')[
                                                               len(str(self.endpoint).split('/')) - 1])):
                    resource = from_db_row_to_object(resource)
                    # checking if the searched resource has the url's path inside her attribute 'uri'
                    if request.url.split(self.endpoint)[1] == resource.get_uri() or \
                            request.url.split(self.endpoint)[1] == '/' + resource.get_uri():
                        self.myDB.execute_query(delete_row_resource_table(resource))
                        return Response(status=204, headers={"Location": request.url})
                return {'ERROR': "Resource Not Found!"}, 404

            except JSONDecodeError:
                return {'ERROR': "Invalid JSON! Check the request"}, 400

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
