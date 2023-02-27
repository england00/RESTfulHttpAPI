from models.resource_model import ResourceModel
from models.picking_system_model import PickingSystemModel


def create_resource_table():
    return """
        CREATE TABLE resource (
        uuid VARCHAR(100) NOT NULL,
        name VARCHAR(100),
        version INT,
        unit VARCHAR(100),
        topic VARCHAR(100) NOT NULL,
        uri VARCHAR(100) NOT NULL,
        qos INT, 
        retained VARCHAR(100),
        frequency INT,
        value VARCHAR(100), 
        picking_system VARCHAR(100) NOT NULL,
        PRIMARY KEY (uuid));
        """


def relation_resource_and_picking_system_table():
    return """
        ALTER TABLE resource
        ADD FOREIGN KEY(picking_system)
        REFERENCES picking_system(pick_and_place_id)
        ON DELETE SET NULL;
        """


def insert_row_resource_table(resource, system):
    if isinstance(resource, ResourceModel) and isinstance(system, PickingSystemModel):
        return """
            INSERT INTO resource (uuid, name, version, unit, topic, uri, qos, retained, frequency, value, picking_system) 
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
            """.format(resource.get_uuid(), str(resource.get_name()).replace("'", ""), resource.get_version(),
                       str(resource.get_unit()).replace("'", ""), str(resource.get_topic()).replace("'", ""),
                       str(resource.get_uri()).replace("'", ""), resource.get_qos(), resource.get_retained(),
                       resource.get_frequency(), str(resource.get_value()).replace("'", ""),
                       str(system.get_pick_and_place_id()))
    else:
        raise TypeError("Error adding new resource. Only ResourceModel and PickingSystemModel objects are allowed")


def delete_resource_table():
    return """
        DROP TABLE resource
        """
