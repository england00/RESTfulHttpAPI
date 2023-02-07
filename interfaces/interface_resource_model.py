import abc


class IResourceModel(abc.ABC):
    @staticmethod
    def from_creation_dto(resource_creation_request):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass
