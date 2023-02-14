from database.database import MySQLDatabase
from models.device_model import DeviceModel

# PARAMS
host = "localhost"
user = "root"
password = "HakertzDB32!"
database = "devices"
charset = "utf8"
device_model = DeviceModel()

if __name__ == "__main__":
    myDB = MySQLDatabase(host, user, password, charset)

    # STARTING CONNECTION
    myDB.start_connection()

    # DATABASE CREATION
    '''
    myDB.create_database(database)
    '''

    # CHOOSING DATABASE
    myDB.choose_database(database)

    # ADDING TABLE
    '''
    create_device_table = device_model.to_SQL()
    myDB.execute_query(create_device_table)
    '''

    # REMOVING TABLE
    '''
    delete_device_table = """
        DROP TABLE device
        """
    myDB.execute_query(delete_device_table)
    '''

    # ADDING INFO
    adding_device = """
        INSERT INTO device (uuid, name, locationId, type, attributes) VALUES

('2020-10-11 09:52:40', 'servizi', '{ "browser": "Firefox", "os": "Windows", "resolution": { "x": 2560, "y": 1600 } }'),"""

    # CLOSING CONNECTION
    myDB.close_connection()
