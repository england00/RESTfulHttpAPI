import logging
import yaml
from database.model.database_object_manager import get_database
from models.resource_model import ResourceModel
from error.configuration_file_error import ConfigurationFileError


class ResourcesMapper:
    _STR_RESOURCE_CONFIG_FILE = "./config/resources.yaml"

    def __init__(self, config_object=None, config_file_path=None, base_topic=None):
        self._resources = {}
        self.myDB = get_database()

        if config_object is not None:
            self._mapper = config_object
        elif config_file_path is not None:
            try:
                with open(config_file_path, 'r') as file:
                    self._mapper = yaml.safe_load(file)
            except Exception as e:
                logging.error(str(e))
                raise ConfigurationFileError("Error while reading configuration file") from None
        else:
            try:
                with open(self._STR_RESOURCE_CONFIG_FILE, 'r') as file:
                    self._mapper = yaml.safe_load(file)
            except Exception as e:
                logging.error(str(e))
                raise ConfigurationFileError("Error while reading configuration") from None

        try:
            for key in self._mapper["resources"]:
                self._resources[key] = ResourceModel.object_mapping(self._mapper["resources"][key])
                if base_topic is not None:
                    self._resources[key].set_topic(base_topic + self._resources[key].get_topic())
        except Exception as e:
            logging.error(str(e))
            raise ConfigurationFileError("Error while parsing configuration data") from None

    def get_resource(self, key):
        return self._resources[key]

    def get_resources(self):

        '''
        query = """
            SELECT *
            FROM resources
        """
        results = self.myDB.read_query(query)
        for result in results:
            print(result)
        '''

        return self._resources

    def set_resources(self, resources):
        self._resources = resources

    def add_resource(self, new_resource):
        if isinstance(new_resource, ResourceModel):
            self._resources[new_resource.uuid] = new_resource

            adding_resource = """
                INSERT INTO resources (uuid, name, version, unit, topic, uri, qos, retained, frequency, value) VALUES
                ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
            """.format(new_resource.get_uuid(), new_resource.get_name(), new_resource.get_version(),
                       new_resource.get_unit(), new_resource.get_topic(), new_resource.get_uri(),
                       new_resource.get_qos(), new_resource.get_retained(), new_resource.get_frequency(),
                       new_resource.get_value())
            self.myDB.execute_query(adding_resource)

        else:
            raise TypeError("Error adding new resource. Only ResourceModel objects are allowed")

    def update_resource(self, update_resource):
        if isinstance(update_resource, ResourceModel):
            self._resources[update_resource.uuid] = update_resource
        else:
            raise TypeError("Error updating the resource. Only ResourceModel objects are allowed")

    def remove_resource(self, key):
        if key in self._resources.keys():
            del self._resources[key]

    # CHOOSING DATABASE
    # self.myDB.choose_database(self.myDB.choosen_database)
