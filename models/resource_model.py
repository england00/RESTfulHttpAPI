from interfaces.models.interface_resource_model import IResourceModel
import json


class ResourceModel(IResourceModel):

    def __init__(self, *args):
        self.uuid = None
        self.version = None
        self.unit = None
        self.topic = None
        self.path = None
        self.qos = None
        self.retained = None
        self.frequency = None
        self.value = None

        if len(args) > 0 and isinstance(args[0], dict):
            vars(self).update(args[0])

    def get_uuid(self):
        return self.uuid

    def get_version(self):
        return self.version

    def get_unit(self):
        return self.unit

    def get_topic(self):
        return self.topic

    def get_path(self):
        return self.path

    def get_qos(self):
        return self.qos

    def get_retained(self):
        return self.retained

    def get_frequency(self):
        return self.frequency

    def get_value(self):
        return self.value

    def set_uuid(self, uuid):
        self.uuid = uuid

    def set_version(self, version):
        self.version = version

    def set_unit(self, unit):
        self.unit = unit

    def set_topic(self, topic):
        self.topic = topic

    def set_path(self, path):
        self.path = path

    def set_qos(self, qos):
        self.qos = qos

    def set_retained(self, retained):
        self.retained = retained

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return f'ResourceModel(' \
               f'{self.uuid},' \
               f'{self.version},' \
               f'{self.unit},' \
               f'{self.topic},' \
               f'{self.path},' \
               f'{self.qos},' \
               f'{self.retained},' \
               f'{self.frequency},' \
               f'{self.value})'

    @staticmethod
    def object_mapping(dictionary):
        return json.loads(json.dumps(dictionary), object_hook=ResourceModel)

    def to_SQL(self):
        return """
            CREATE TABLE resources (
            uuid VARCHAR(40) NOT NULL,
            version INT,
            unit VARCHAR(10),
            topic VARCHAR(100)
            path VARCHAR(100),
            qou INT, 
            retained VARCHAR(5),
            frequency INT,
            value VARCHAR(40), 
            PRIMARY KEY (uuid));
            """
