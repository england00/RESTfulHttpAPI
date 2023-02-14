import abc


class IResourceModel(abc.ABC):

    @abc.abstractmethod
    def get_uuid(self):
        pass

    @abc.abstractmethod
    def get_version(self):
        pass

    @abc.abstractmethod
    def get_unit(self):
        pass

    @abc.abstractmethod
    def get_topic(self):
        pass

    @abc.abstractmethod
    def get_qos(self):
        pass

    @abc.abstractmethod
    def get_retained(self):
        pass

    @abc.abstractmethod
    def get_frequency(self):
        pass

    @abc.abstractmethod
    def get_value(self):
        pass

    @abc.abstractmethod
    def set_uuid(self, uuid):
        pass

    @abc.abstractmethod
    def set_version(self, version):
        pass

    @abc.abstractmethod
    def set_unit(self, unit):
        pass

    @abc.abstractmethod
    def set_topic(self, topic):
        pass

    @abc.abstractmethod
    def set_qos(self, qos):
        pass

    @abc.abstractmethod
    def set_retained(self, retained):
        pass

    @abc.abstractmethod
    def set_frequency(self, frequency):
        pass

    @abc.abstractmethod
    def set_value(self, value):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass
