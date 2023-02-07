import socket
import requests
import creation_request.resource_creation_request
from flask import Flask
from flask_restful import Api
from models.device_model import DeviceModel
from persistence.data_manager import DataManager
from resources.resources_methods import Resources
from resources.resource_methods import SingleResource

# creating a Flask application
app = Flask(__name__)
api = Api(app)
ENDPOINT_PREFIX = "/api/iot/inventory"
print("Starting HTTP RESTful API Server ...")


# FOR EACH RESOURCE MODEL
# BEGIN

# creating an object DataManager
deviceDataManager = DataManager()

# creating an object DeviceModel
device00001 = DeviceModel("device00001", "Temperature Sensor", "000001", "dev:dummy:temperature",
                          {"min_value": -200,
                           "unit": "C",
                           "software_version": "0.0.1",
                           "battery": False,
                           "manufacturer": "ACME Corporation",
                           "max_value": 200})

device00002 = DeviceModel("device00002", "Position Sensor", "000001", "dev:dummy:position",
                          {"precision": 0.025,
                           "unit": "m",
                           "software_version": "0.0.1",
                           "battery": True,
                           "manufacturer": "ACME Corporation"})

device00003 = DeviceModel("device00003", "Humidity Sensor", "000001", "dev:dummy:humidity",
                          {"min_value": 0,
                           "unit": "m",
                           "software_version": "0.0.1",
                           "battery": False,
                           "manufacturer": "ACME Corporation",
                           "max_value": 100})

# adding new devices inside the DataManager object
deviceDataManager.add_device(device00001)
deviceDataManager.add_device(device00002)
deviceDataManager.add_device(device00003)

# setting models type
creation_request.resource_creation_request.setModel("device")
creation_request.resource_creation_request.modifyIResourceCreationRequest()

# adding the Resources class for "device" to the api
api.add_resource(Resources, ENDPOINT_PREFIX + '/device',
                 resource_class_kwargs={'data_manager': deviceDataManager},
                 endpoint="devices",
                 methods=['GET', 'POST'])

# adding the SingleResource class for "device" to the api
api.add_resource(SingleResource, ENDPOINT_PREFIX + '/device/<string:resource_id>',
                 resource_class_kwargs={'data_manager': deviceDataManager},
                 endpoint='device',
                 methods=['GET', 'PUT', 'DELETE'])

# END


# printing local and public IPs
localIp = socket.gethostbyname(socket.gethostname())
publicIp = requests.get('https://checkip.amazonaws.com').text.strip()
localhost = "127.0.0.1"
broadcastIp = "0.0.0.0"

# executing the code (https with self-signed certificate)
if __name__ == '__main__':
    app.run(ssl_context='adhoc', host=broadcastIp, port=7070)  # run our Flask app
