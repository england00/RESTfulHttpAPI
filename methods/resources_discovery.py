from interfaces.resources.interface_resources_discovery import IResourcesDiscovery


class ResourcesDiscovery(IResourcesDiscovery):

    def __init__(self, **kwargs):
        self.system_mapper = kwargs['system_mapper']
        self.endpoint = kwargs['endpoint']

    # GET method: obtaining the list in json format of all the system inside the database
    def get(self):
        try:
            # iterate over the dictionary to build a serializable resource list
            system_list = []
            for system in self.system_mapper.get_systems().values():
                system_dict = system.__dict__
                del system_dict["resources_mapper"]
                del system_dict["path_list"]
                system_list.append(system_dict)

            # checking not having an empty list
            if len(system_list) != 0:
                return system_list, 200  # return data and 200 OK code
            return {'ERROR': "Resources Not Found!"}, 404

        except Exception as e:
            return {'ERROR': "Generic Internal Server Error! Reason: " + str(e)}, 500
