from database.model.database import MySQLDatabase
from database.queries.picking_system_queries import *
from database.queries.resource_queries import *

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

    # CHOOSING DATABASE
    myDB.choose_database(chosen_database)

    # REMOVING TABLES
    myDB.execute_query(delete_resource_table())
    myDB.execute_query(delete_picking_system_table())

    # DROPPING DATABASE
    myDB.destroy_database(chosen_database)

    # CLOSING CONNECTION
    myDB.close_connection()
