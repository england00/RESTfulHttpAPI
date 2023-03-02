import socket
import requests
from flask import Flask
from flask_restful import Api
from resources.resources_methods import Resources
from resources.resource_methods import SingleResource
from models.picking_systems_mapper import PickingSystemsMapper
from database.model.database import MySQLDatabase


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MYSQL # ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# database params
host = "localhost"
user = "root"
password = "HakertzDB32!"
charset = "utf8"
chosen_database = "api_database"

# creating a MySQLDatabase object
myDB = MySQLDatabase(host, user, password, charset)

# opening connection with MySQL and choosing the right database
myDB.start_connection()
myDB.choose_database(chosen_database)


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------- # PICKING SYSTEM MAPPER # --------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# creating an object PickingSystemsMapper
picking_system_mapper = PickingSystemsMapper(myDB)


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # FLASK # ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# creating a Flask application
app = Flask(__name__)
api = Api(app)
ENDPOINT_PREFIX = "/api/iot"
print("Starting HTTP RESTful API Server ...")

# finding all the resources_mappers, one for each picking system
for system in picking_system_mapper.get_systems().values():

    # declaring endpoint path list
    endpoint_path_list = [['', 'all', 'single']]
    for p in system.get_resource_path_list():
        endpoint_path_list.append([p, 'all-' + p, 'single-' + p])

    # adding Resources and SingleResource class with all the endpoints list
    for ept in endpoint_path_list:
        api.add_resource(Resources, ENDPOINT_PREFIX + system.get_endpoint() + ept[0],
                         resource_class_kwargs={'resources_mapper': system.get_resource_mapper(),
                                                'endpoint': str(ENDPOINT_PREFIX + system.get_endpoint())},
                         endpoint=ept[1] + "-" + system.get_endpoint(),
                         methods=['GET', 'POST'])
        api.add_resource(SingleResource, ENDPOINT_PREFIX + system.get_endpoint() + ept[0] + '/<string:resource_id>',
                         resource_class_kwargs={'resources_mapper': system.get_resource_mapper(),
                                                'endpoint': str(ENDPOINT_PREFIX + system.get_endpoint())},
                         endpoint=ept[2] + "-" + system.get_endpoint(),
                         methods=['GET', 'PUT', 'DELETE'])

# storing local and public IPs
localIp = socket.gethostbyname(socket.gethostname())
publicIp = requests.get('https://checkip.amazonaws.com').text.strip()
localhost = "127.0.0.1"
broadcastIp = "0.0.0.0"


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MAIN # ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

# executing the code (https with self-signed certificate)
if __name__ == '__main__':
    # Flask application
    app.run(ssl_context='adhoc', host=broadcastIp, port=7070)

    # closing connection with MySQL
    myDB.close_connection()
