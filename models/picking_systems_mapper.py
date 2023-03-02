from database.model.database_object_manager import get_database
from database.queries.picking_system_queries import *
from models.resources_mapper import ResourcesMapper

myDB = get_database()


class PickingSystemsMapper:

    def __init__(self):
        self.picking_system_dictionary = {}

        for system in myDB.read_query(showing_picking_system_table()):
            picking_system_model = PickingSystemModel(pick_and_place_id=str(system[0]),
                                                      endpoint=str(system[1]),
                                                      resource_mapper=ResourcesMapper(initialization=True,
                                                                                      system_id=system[0]))
            self.picking_system_dictionary[picking_system_model.pick_and_place_id] = picking_system_model

    def get_systems(self):
        return self.picking_system_dictionary

    def add_system(self, newPickingSystem):
        if isinstance(newPickingSystem, PickingSystemModel):  # check data type
            if newPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                raise TypeError("ERROR adding new system! This ID already exists!")
            else:
                self.picking_system_dictionary[newPickingSystem.pick_and_place_id] = newPickingSystem
                myDB.execute_query(insert_row_picking_system_table(newPickingSystem))
        else:
            raise TypeError("ERROR adding new device! Only PickingSystemModel are allowed!")

    def update_system(self, updatedPickingSystem):
        if isinstance(updatedPickingSystem, PickingSystemModel):  # check data type
            if updatedPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                self.picking_system_dictionary[updatedPickingSystem.pick_and_place_id] = updatedPickingSystem
            else:
                raise TypeError("ERROR updating the system! This ID doesn't exists!")
            self.picking_system_dictionary[updatedPickingSystem.pick_and_place_id] = updatedPickingSystem
        else:
            raise TypeError("ERROR updating the device! Only PickingSystemModel are allowed!")

    def remove_system(self, pick_and_place_id):
        if pick_and_place_id in self.picking_system_dictionary.keys():
            if pick_and_place_id in self.picking_system_dictionary.keys():
                del self.picking_system_dictionary[pick_and_place_id]
            else:
                raise TypeError("ERROR deleting the system! This ID doesn't exists!")
