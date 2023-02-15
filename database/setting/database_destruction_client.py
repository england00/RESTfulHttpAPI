from database.model.database_object_manager import get_database

# receiving a MySQLDatabase object
myDB = get_database()

if __name__ == "__main__":
    # STARTING CONNECTION
    myDB.start_connection()

    # CHOOSING DATABASE
    myDB.choose_database(myDB.choosen_database)

    # REMOVING TABLE
    delete_device_table = """
        DROP TABLE resources
    """
    myDB.execute_query(delete_device_table)

    # DROPPING DATABASE
    myDB.destroy_database(myDB.choosen_database)

    # CLOSING CONNECTION
    myDB.close_connection()
