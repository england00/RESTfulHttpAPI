import abc
from flask_restful import Resource


class IResourcesDiscovery(Resource):

    @abc.abstractmethod
    def get(self):
        pass
