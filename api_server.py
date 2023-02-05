from flask import Flask
from flask_restful import Api
from resources.device_resource import DeviceResource
from resources.devices_resource import DevicesResource
from model.device_model import DeviceModel
from persistence.data_manager import DataManager
import socket

app = Flask(__name__)
api = Api(app)

ENDPOINT_PREFIX = "/api/iot/inventory"

print("Starting HTTP RESTful API Server ...")

# creating an object DataManager
dataManager = DataManager()

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
dataManager.add_device(device00001)
dataManager.add_device(device00002)
dataManager.add_device(device00003)

# adding the DevicesResource class to the api
api.add_resource(DevicesResource, ENDPOINT_PREFIX + '/device',
                 resource_class_kwargs={'data_manager': dataManager},
                 endpoint="devices",
                 methods=['GET', 'POST'])

# adding the DeviceResource class to the api
api.add_resource(DeviceResource, ENDPOINT_PREFIX + '/device/<string:device_id>',
                 resource_class_kwargs={'data_manager': dataManager},
                 endpoint='device',
                 methods=['GET', 'PUT', 'DELETE'])

# printing local and public IPs
localIp = socket.gethostbyname(socket.gethostname())
localhost = "127.0.0.1"
broadcastIp = "0.0.0.0"

# executing the code (https with self-signed certificate)
if __name__ == '__main__':
    app.run(ssl_context='adhoc', host=broadcastIp, port=7070)  # run our Flask app
