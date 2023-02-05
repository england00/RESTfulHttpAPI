from flask import Flask
from flask_restful import Resource, Api, reqparse
from resources.device_resource import DeviceResource
from resources.devices_resource import DevicesResource
from persistence.data_manager import DataManager
import socket, requests

app = Flask(__name__)
api = Api(app)

ENDPOINT_PREFIX = "/api/iot/inventory"

print("Starting HTTP RESTful API Server ...")

dataManager = DataManager()

api.add_resource(DevicesResource, ENDPOINT_PREFIX + '/device',
                 resource_class_kwargs={'data_manager': dataManager},
                 endpoint="devices",
                 methods=['GET', 'POST'])

api.add_resource(DeviceResource, ENDPOINT_PREFIX + '/device/<string:device_id>',
                resource_class_kwargs={'data_manager': dataManager},
                 endpoint='device',
                 methods=['GET', 'PUT', 'DELETE'])

localIp = socket.gethostbyname(socket.gethostname())
print("Il mio indirizzo IP locale:", localIp)
publicIp = requests.get('https://checkip.amazonaws.com').text.strip()
print("Il mio indirizzo IP pubblico:", publicIp)

if __name__ == '__main__':
    app.run(ssl_context='adhoc', host=localIp, port=7070)  # run our Flask app