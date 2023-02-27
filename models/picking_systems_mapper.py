from models.picking_system_model import PickingSystemModel


class PickingSystemsMapper:
    picking_system_dictionary = {}

    def get_systems(self):
        return self.picking_system_dictionary

    def add_system(self, newPickingSystem):
        if isinstance(newPickingSystem, PickingSystemModel):  # check data type
            if newPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                raise TypeError("ERROR adding new system! This ID already exists!")
            else:
                self.picking_system_dictionary[newPickingSystem.pick_and_place_id] = newPickingSystem
        else:
            raise TypeError("ERROR adding new device! Only DeviceModel are allowed!")

    def update_system(self, updatedPickingSystem):
        if isinstance(updatedPickingSystem, PickingSystemModel):  # check data type
            if updatedPickingSystem.get_pick_and_place_id() in self.picking_system_dictionary.keys():
                self.picking_system_dictionary[updatedPickingSystem.pick_and_place_id] = updatedPickingSystem
            else:
                raise TypeError("ERROR updating the system! This ID doesn't exists!")
            self.picking_system_dictionary[updatedPickingSystem.pick_and_place_id] = updatedPickingSystem
        else:
            raise TypeError("ERROR updating the device! Only DeviceModel are allowed!")

    def remove_system(self, pick_and_place_id):
        if pick_and_place_id in self.picking_system_dictionary.keys():
            if pick_and_place_id in self.picking_system_dictionary.keys():
                del self.picking_system_dictionary[pick_and_place_id]
            else:
                raise TypeError("ERROR deleting the system! This ID doesn't exists!")
