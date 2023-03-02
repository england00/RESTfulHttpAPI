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
        PRIMARY KEY (uuid, picking_system));
        """


def relation_resource_and_picking_system_table():
    return """
        ALTER TABLE resource
        ADD FOREIGN KEY(picking_system)
        REFERENCES picking_system(pick_and_place_id)
        ON DELETE SET NULL;
        """


def showing_resource_table_join_system(system_name):
    return """SELECT * 
              FROM resource
              WHERE picking_system = {}
           """.format(str(system_name))


def insert_row_resource_table(resource, system):
    if isinstance(resource, ResourceModel):
        if isinstance(system, PickingSystemModel):
            return """
                INSERT INTO resource (uuid, name, version, unit, topic, uri, qos, retained, frequency, value, 
                picking_system) 
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
                """.format(str(resource.get_uuid()), str(resource.get_name()).replace("'", ""), resource.get_version(),
                           str(resource.get_unit()).replace("'", ""), str(resource.get_topic()).replace("'", ""),
                           str(resource.get_uri()).replace("'", ""), resource.get_qos(), resource.get_retained(),
                           resource.get_frequency(), str(resource.get_value()).replace("'", ""),
                           str(system.get_pick_and_place_id()))
        else:
            return """
                INSERT INTO resource (uuid, name, version, unit, topic, uri, qos, retained, frequency, value, 
                picking_system) 
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(str(resource.get_uuid()), str(resource.get_name()).replace("'", ""), resource.get_version(),
                           str(resource.get_unit()).replace("'", ""), str(resource.get_topic()).replace("'", ""),
                           str(resource.get_uri()).replace("'", ""), resource.get_qos(), resource.get_retained(),
                           resource.get_frequency(), str(resource.get_value()).replace("'", ""),
                           str(resource.get_picking_system()))
    else:
        raise TypeError("Error adding new resource. Only ResourceModel objects are allowed")


def modify_row_resource_table(resource):
    if isinstance(resource, ResourceModel):
        return """
            UPDATE resource
            SET name = '{}', version = '{}', unit = '{}', topic = '{}', uri = '{}', qos = '{}', retained = '{}', 
            frequency = '{}', value = '{}'
            WHERE (uuid = '{}' AND picking_system = '{}');
            """.format(str(resource.get_name()).replace("'", ""), resource.get_version(),
                       str(resource.get_unit()).replace("'", ""), str(resource.get_topic()).replace("'", ""),
                       str(resource.get_uri()).replace("'", ""), resource.get_qos(), resource.get_retained(),
                       resource.get_frequency(), str(resource.get_value()).replace("'", ""),
                       str(resource.get_uuid()), str(resource.get_picking_system()))
    else:
        raise TypeError("Error adding new resource. Only ResourceModel objects are allowed")


def delete_row_resource_table(resource):
    if isinstance(resource, ResourceModel):
        return """
            DELETE
            FROM resource
            WHERE (uuid = '{}' AND picking_system = '{}')
            """.format(str(resource.get_uuid()), str(resource.get_picking_system()))
    else:
        raise TypeError("Error adding new resource. Only ResourceModel objects are allowed")


def delete_resource_table():
    return """
        DROP TABLE resource
        """
