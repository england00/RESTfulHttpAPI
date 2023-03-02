import logging
import yaml
from database.model.database import MySQLDatabase
from database.queries.picking_system_queries import *
from database.queries.resource_queries import *
from error.configuration_file_error import ConfigurationFileError

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

    # CHOOSING DATABASE
    myDB.choose_database(db_params["chosen_database"])

    # REMOVING TABLES
    myDB.execute_query(delete_resource_table())
    myDB.execute_query(delete_picking_system_table())

    # DROPPING DATABASE
    myDB.destroy_database(db_params["chosen_database"])

    # CLOSING CONNECTION
    myDB.close_connection()
