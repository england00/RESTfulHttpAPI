import socket
import requests
from flask import Flask
from flask_restful import Api
from resources.resources_methods import Resources
from resources.resource_methods import SingleResource
from database.database import MySQLDatabase
from models.resource_mapper import ResourcesMapper

# creating a Flask application
app = Flask(__name__)
api = Api(app)
ENDPOINT_PREFIX = "/api/iot/"
print("Starting HTTP RESTful API Server ...")

# creating an object ResourcesMapper
resources_mapper = ResourcesMapper()  # already configured with './config/resources.yaml'

# adding the Resources class for "device" to the api
api.add_resource(Resources, ENDPOINT_PREFIX + '/resources',
                 resource_class_kwargs={'resources_mapper': resources_mapper},
                 endpoint="resources",
                 methods=['GET', 'POST'])

# adding the SingleResource class for "device" to the api
api.add_resource(SingleResource, ENDPOINT_PREFIX + '/resources/<string:resource_id>',
                 resource_class_kwargs={'resources_mapper': resources_mapper},
                 endpoint='resource',
                 methods=['GET', 'PUT', 'DELETE'])

# database params
host = "localhost"
user = "root"
password = "HakertzDB32!"
database = "devices"
charset = "utf8"

# printing local and public IPs
localIp = socket.gethostbyname(socket.gethostname())
publicIp = requests.get('https://checkip.amazonaws.com').text.strip()
localhost = "127.0.0.1"
broadcastIp = "0.0.0.0"

# executing the code (https with self-signed certificate)
if __name__ == '__main__':
    myDB = MySQLDatabase(host, user, password, charset)
    myDB.start_connection()

    app.run(ssl_context='adhoc', host=broadcastIp, port=7070)  # run our Flask app
