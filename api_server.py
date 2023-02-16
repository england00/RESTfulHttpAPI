import socket
import requests
from flask import Flask
from flask_restful import Api
from resources.resources_methods import Resources
from resources.resource_methods import SingleResource
from database.model.database_object_manager import get_database
from models.resource_mapper import ResourcesMapper


# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------- # RESOURCE MAPPER # ------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

# creating an object ResourcesMapper
resources_mapper = ResourcesMapper()  # already configured with './config/resources.yaml'

# saving uri's path
path_list = [resource.get_uri().replace('/{}'.format(
    resource.get_uri().split('/')[len(resource.get_uri().split('/')) - 1]), "")
    for resource in resources_mapper.get_resources().values()]

# managing the absence of '/' at the beginning of the path
for i in range(len(path_list)):
    if path_list[i][0] != '/':
        path_list[i] = '/' + path_list[i]

# removing duplicates
single_list = []
for p in path_list:
    if p not in single_list:
        single_list.append(p)
path_list = single_list


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # FLASK # ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# creating a Flask application
app = Flask(__name__)
api = Api(app)
ENDPOINT_PREFIX = "/api/iot/"
print("Starting HTTP RESTful API Server ...")

# declaring endpoint path list
endpoint_path_list = [['', 'all', 'single']]
for p in path_list:
    endpoint_path_list.append([p, 'all-' + p, 'single-' + p])

# adding Resources and SingleResource class with all the endpoints list
for ept in endpoint_path_list:
    api.add_resource(Resources, ENDPOINT_PREFIX + ept[0],
                     resource_class_kwargs={'resources_mapper': resources_mapper},
                     endpoint=ept[1],
                     methods=['GET', 'POST'])
    api.add_resource(SingleResource, ENDPOINT_PREFIX + ept[0] + '/<string:resource_id>',
                     resource_class_kwargs={'resources_mapper': resources_mapper},
                     endpoint=ept[2],
                     methods=['GET', 'PUT', 'DELETE'])

# printing local and public IPs
localIp = socket.gethostbyname(socket.gethostname())
publicIp = requests.get('https://checkip.amazonaws.com').text.strip()
localhost = "127.0.0.1"
broadcastIp = "0.0.0.0"


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MYSQL # ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# receiving a MySQLDatabase object
myDB = get_database()


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MAIN # ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

# executing the code (https with self-signed certificate)
if __name__ == '__main__':
    # opening connection with MySQL and choosing the right database
    myDB.start_connection()
    myDB.choose_database(myDB.choosen_database)

    # Flask application
    app.run(ssl_context='adhoc', host=broadcastIp, port=7070)

    # closing connection with MySQL
    myDB.close_connection()
