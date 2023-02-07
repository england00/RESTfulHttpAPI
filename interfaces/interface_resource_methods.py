import abc
from flask_restful import Resource


class IRequests(Resource):

    @abc.abstractmethod
    def get(self, resource_id):
        pass

    @abc.abstractmethod
    def put(self, resource_id):
        pass

    @abc.abstractmethod
    def delete(self, resource_id):
        pass
