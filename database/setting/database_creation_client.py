from database.model.database_object_manager import get_database
from models.resource_model import ResourceModel

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
    create_device_table = ResourceModel.to_SQL()
    myDB.execute_query(create_device_table)

    # CLOSING CONNECTION
    myDB.close_connection()
