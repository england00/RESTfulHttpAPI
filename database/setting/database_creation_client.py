from database.model.database import MySQLDatabase
from database.queries.picking_system_queries import *
from database.queries.resource_queries import *
from models.resources_mapper import ResourcesMapper

# database params
host = "localhost"
user = "root"
password = "HakertzDB32!"
charset = "utf8"
chosen_database = "api_database"

# creating a MySQLDatabase object
myDB = MySQLDatabase(host, user, password, charset)

if __name__ == "__main__":

    # STARTING CONNECTION
    myDB.start_connection()

    # DATABASE CREATION
    myDB.create_database(chosen_database)

    # CHOOSING DATABASE
    myDB.choose_database(chosen_database)

    # TABLE CREATION
    myDB.execute_query(create_picking_system_table())
    myDB.execute_query(create_resource_table())
    myDB.execute_query(relation_resource_and_picking_system_table())

    # INSERTING ROWS IN PICKING SYSTEM TABLE
    system1 = PickingSystemModel(pick_and_place_id='000001', endpoint='/000001',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml", database=myDB))
    myDB.execute_query(insert_row_picking_system_table(system1))

    system2 = PickingSystemModel(pick_and_place_id='000002', endpoint='/000002',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml", database=myDB))
    myDB.execute_query(insert_row_picking_system_table(system2))

    system3 = PickingSystemModel(pick_and_place_id='000003', endpoint='/pippo',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml", database=myDB))
    myDB.execute_query(insert_row_picking_system_table(system3))

    # INSERTING ROWS IN RESOURCE TABLE
    for resource in system1.get_resource_mapper().get_resources().values():
        myDB.execute_query(insert_row_resource_table(resource, system1))

    for resource in system1.get_resource_mapper().get_resources().values():
        myDB.execute_query(insert_row_resource_table(resource, system2))

    for resource in system1.get_resource_mapper().get_resources().values():
        myDB.execute_query(insert_row_resource_table(resource, system3))

    # PRINTING SYSTEMS TABLE
    # SYSTEM1
    list1 = myDB.read_query(showing_resource_table_join_system('000001'))
    for resource in list1:
        print(resource)

    # SYSTEM2
    list2 = myDB.read_query(showing_resource_table_join_system('000002'))
    for resource in list2:
        print(resource)

    # SYSTEM3
    list3 = myDB.read_query(showing_resource_table_join_system('000003'))
    for resource in list3:
        print(resource)

    # CLOSING CONNECTION
    myDB.close_connection()
