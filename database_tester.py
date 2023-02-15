from database.model.database import MySQLDatabase
from models.resource_model import ResourceModel

# PARAMS
host = "localhost"
user = "root"
password = "HakertzDB32!"
database = "api_database"
charset = "utf8"
resource_model = ResourceModel()

if __name__ == "__main__":
    myDB = MySQLDatabase(host, user, password, charset, database)

    # STARTING CONNECTION
    myDB.start_connection()

    # DATABASE CREATION
    myDB.create_database(database)

    # CHOOSING DATABASE
    myDB.choose_database(database)

    # ADDING TABLE
    create_device_table = resource_model.to_SQL()
    myDB.execute_query(create_device_table)


    # REMOVING TABLE
    delete_device_table = """
        DROP TABLE resources
        """
    myDB.execute_query(delete_device_table)

    # ADDING INFO
    adding_device = """
        INSERT INTO device (uuid, name, locationId, type, attributes) VALUES

('2020-10-11 09:52:40', 'servizi', '{ "browser": "Firefox", "os": "Windows", "resolution": { "x": 2560, "y": 1600 } }'),"""

    # DROPPING DATABASE
    myDB.destroy_database(database)

    # CLOSING CONNECTION
    myDB.close_connection()
