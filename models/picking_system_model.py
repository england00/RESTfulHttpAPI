from interfaces.models.interface_picking_system_model import IPickingSystemModel
import json


class PickingSystemModel(IPickingSystemModel):

    def __init__(self, *args):
        self.pick_and_place_id = args[0]
        self.endpoint = args[1]
        self.resources_mapper = args[2]
        self.path_list = None
        self.resource_path_list = None
        self.obtaining_path_list()
        self.obtaining_resource_path_list()

        if len(args) > 0 and isinstance(args[0], dict):
            vars(self).update(args[0])

    def get_pick_and_place_id(self):
        return self.pick_and_place_id

    def get_endpoint(self):
        return self.endpoint

    def get_resource_mapper(self):
        return self.resources_mapper

    def get_path_list(self):
        return self.path_list

    def get_resource_path_list(self):
        return self.resource_path_list

    def set_pick_and_place_id(self, pick_and_place_id):
        self.pick_and_place_id = pick_and_place_id

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def set_resource_mapper(self, resource_mapper):
        self.resources_mapper = resource_mapper

    def set_path_list(self, path_list):
        self.path_list = path_list

    def set_resource_path_list(self, resource_path_list):
        self.resource_path_list = resource_path_list

    def obtaining_path_list(self):
        if self.resources_mapper is not None:

            # saving uri's path inside the resource mapper
            self.path_list = [resource.get_uri().replace('/{}'.format(
                resource.get_uri().split('/')[len(resource.get_uri().split('/')) - 1]), "")
                for resource in self.resources_mapper.get_resources().values()]

            # managing the absence of '/' at the beginning of the path
            for i in range(len(self.path_list)):
                if self.path_list[i][0] != '/':
                    self.path_list[i] = '/' + self.path_list[i]

            # removing duplicates
            single_list = []
            for p in self.path_list:
                if p not in single_list:
                    single_list.append(p)
            self.path_list = single_list

    def obtaining_resource_path_list(self):
        if self.resources_mapper is not None:

            # saving uri's path inside the resource mapper
            self.resource_path_list = [resource.get_uri() for resource in
                                       self.resources_mapper.get_resources().values()]

            # managing the absence of '/' at the beginning of the path
            for i in range(len(self.resource_path_list)):
                if self.resource_path_list[i][0] != '/':
                    self.resource_path_list[i] = '/' + self.resource_path_list[i]

    def __str__(self):
        return f'PickingSystemModel(' \
               f'{self.pick_and_place_id},' \
               f'{self.endpoint},' \
               f'{self.resources_mapper})'

    @staticmethod
    def object_mapping(dictionary):
        print(dictionary)
        return json.loads(json.dumps(dictionary), object_hook=PickingSystemModel)
