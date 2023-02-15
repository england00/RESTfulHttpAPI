from database.model.database import MySQLDatabase

# database params
host = "localhost"
user = "root"
password = "HakertzDB32!"
charset = "utf8"
choosen_database = "api_database"

# creating a MySQLDatabase object
database = MySQLDatabase(host, user, password, charset, choosen_database)


# getting database from this module
def get_database():
    global database
    return database
