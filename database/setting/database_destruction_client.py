from database.model.database_object_manager import get_database
from database.queries.picking_system_queries import *
from database.queries.resource_queries import *

# receiving a MySQLDatabase object
myDB = get_database()

if __name__ == "__main__":
    # STARTING CONNECTION
    myDB.start_connection()

    # CHOOSING DATABASE
    myDB.choose_database(myDB.choosen_database)

    # REMOVING TABLES
    myDB.execute_query(delete_resource_table())
    myDB.execute_query(delete_picking_system_table())

    # DROPPING DATABASE
    myDB.destroy_database(myDB.choosen_database)

    # CLOSING CONNECTION
    myDB.close_connection()
