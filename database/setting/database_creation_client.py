from database.model.database_object_manager import get_database
from database.queries.picking_system_queries import *
from database.queries.resource_queries import *
from models.resources_mapper import ResourcesMapper

# receiving a MySQLDatabase object
myDB = get_database()

if __name__ == "__main__":
    myDB = get_database()

    # STARTING CONNECTION
    myDB.start_connection()

    # DATABASE CREATION
    myDB.create_database(myDB.choosen_database)

    # CHOOSING DATABASE
    myDB.choose_database(myDB.choosen_database)

    # TABLE CREATION
    myDB.execute_query(create_picking_system_table())
    myDB.execute_query(create_resource_table())
    myDB.execute_query(relation_resource_and_picking_system_table())

    # INSERTING ROWS IN PICKING SYSTEM TABLE
    system1 = PickingSystemModel(pick_and_place_id='000001', endpoint='/000001',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml"))
    myDB.execute_query(insert_row_picking_system_table(system1))

    system2 = PickingSystemModel(pick_and_place_id='000002', endpoint='/000002',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml"))
    myDB.execute_query(insert_row_picking_system_table(system2))

    system3 = PickingSystemModel(pick_and_place_id='000003', endpoint='/pippo',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml"))
    myDB.execute_query(insert_row_picking_system_table(system3))

    # INSERTING ROWS IN RESOURCE TABLE
    for resource in system1.get_resource_mapper().get_resources().values():
        myDB.execute_query(insert_row_resource_table(resource, system1))

    for resource in system1.get_resource_mapper().get_resources().values():
        myDB.execute_query(insert_row_resource_table(resource, system2))

    for resource in system1.get_resource_mapper().get_resources().values():
        myDB.execute_query(insert_row_resource_table(resource, system3))


    '''
    print(myDB.read_query("""SELECT *
                       FROM picking_system
                       WHERE pick_and_place_id = '000001'"""))
    print(myDB.read_query("""SELECT *
                           FROM resource"""))
    '''

    # CLOSING CONNECTION
    myDB.close_connection()
