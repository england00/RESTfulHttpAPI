import abc
from flask_restful import Resource


class IRequests(Resource):

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def post(self):
        pass
