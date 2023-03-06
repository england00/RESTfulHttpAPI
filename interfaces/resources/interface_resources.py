import abc
from flask_restful import Resource


class IResources(Resource):

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def post(self):
        pass
