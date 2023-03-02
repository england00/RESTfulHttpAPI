import logging
import yaml
from database.model.database import MySQLDatabase
from database.queries.picking_system_queries import *
from database.queries.resource_queries import *
from error.configuration_file_error import ConfigurationFileError
from models.resources_mapper import ResourcesMapper

# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ # CONFIGURATION # ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

STR_DATABASE_CONFIG_FILE = "../../config/database.yaml"


def configuration_loader(path):
    try:
        with open(path, 'r') as file:
            params = yaml.safe_load(file)
        return params
    except Exception as e:
        logging.error(str(e))
        raise ConfigurationFileError("Error while reading configuration") from None


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MAIN # ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    # LOADING DATABASE CONFIGURATION
    db_params = configuration_loader(STR_DATABASE_CONFIG_FILE)

    # CREATING A MySQLDatabase OBJECT
    myDB = MySQLDatabase(db_params["host"], db_params["user"], db_params["password"], db_params["charset"])

    # STARTING CONNECTION
    myDB.start_connection()

    # DATABASE CREATION
    myDB.create_database(db_params["chosen_database"])

    # CHOOSING DATABASE
    myDB.choose_database(db_params["chosen_database"])

    # TABLE CREATION
    myDB.execute_query(create_picking_system_table())
    myDB.execute_query(create_resource_table())
    myDB.execute_query(relation_resource_and_picking_system_table())

    # INSERTING ROWS IN PICKING SYSTEM TABLE
    system1 = PickingSystemModel(pick_and_place_id='000001', endpoint='/000001',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml",
                                                                 database=myDB))
    myDB.execute_query(insert_row_picking_system_table(system1))

    system2 = PickingSystemModel(pick_and_place_id='000002', endpoint='/000002',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml",
                                                                 database=myDB))
    myDB.execute_query(insert_row_picking_system_table(system2))

    system3 = PickingSystemModel(pick_and_place_id='000003', endpoint='/pippo',
                                 resource_mapper=ResourcesMapper(config_file_path="../../config/resources.yaml",
                                                                 database=myDB))
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
