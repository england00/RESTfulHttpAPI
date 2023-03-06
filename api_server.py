import logging
import yaml
from flask import Flask
from flask_restful import Api
from error.configuration_file_error import ConfigurationFileError
from resources.resources_methods import Resources
from resources.resource_methods import SingleResource
from models.picking_systems_mapper import PickingSystemsMapper
from database.model.database import MySQLDatabase

# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ # CONFIGURATION # ------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

STR_DATABASE_CONFIG_FILE = "./config/database.yaml"
STR_APPLICATION_CONFIG_FILE = "config/application.yaml"


def configuration_loader(path):
    try:
        with open(path, 'r') as file:
            params = yaml.safe_load(file)
        return params
    except Exception as e:
        logging.error(str(e))
        raise ConfigurationFileError("Error while reading configuration") from None


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # FLASK # ----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

def web_application():
    # creating the application
    application = Flask(__name__)
    application_program_interface = Api(application)
    print("Starting HTTP RESTful API Server ...")
    return application, application_program_interface


def resource_mapping(system_mapper, application_program_interface, endpoint_prefix, database):
    # finding all the resources lists, each one for each picking system
    for system in system_mapper.get_systems().values():

        # declaring endpoint path list
        endpoint_path_list = [['', 'all', 'single']]
        for p in system.get_resource_path_list():
            endpoint_path_list.append([p, 'all-' + p, 'single-' + p])

        # adding Resources and SingleResource class with all the endpoints list
        for ept in endpoint_path_list:
            application_program_interface.add_resource(Resources, endpoint_prefix + system.get_endpoint() + ept[0],
                                                       resource_class_kwargs={
                                                           'endpoint': str(endpoint_prefix + system.get_endpoint()),
                                                           'database': database},
                                                       endpoint=ept[1] + "-" + system.get_endpoint(),
                                                       methods=['GET', 'POST'])
            application_program_interface.add_resource(SingleResource, endpoint_prefix + system.get_endpoint() + ept[
                0] + '/<string:resource_id>',
                                                       resource_class_kwargs={
                                                           'endpoint': str(endpoint_prefix + system.get_endpoint()),
                                                           'database': database},
                                                       endpoint=ept[2] + "-" + system.get_endpoint(),
                                                       methods=['GET', 'PUT', 'DELETE'])


# -------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- # MAIN # ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #

# executing the code (https with self-signed certificate)
if __name__ == '__main__':
    # loading database configuration
    db_params = configuration_loader(STR_DATABASE_CONFIG_FILE)

    # creating a MySQLDatabase object
    myDB = MySQLDatabase(db_params["host"], db_params["user"], db_params["password"], db_params["charset"])

    # opening connection with MySQL and choosing the right database
    myDB.start_connection()
    myDB.choose_database(db_params["chosen_database"])

    # creating an object PickingSystemsMapper
    picking_system_mapper = PickingSystemsMapper(myDB)

    # Flask application
    app_params = configuration_loader(STR_APPLICATION_CONFIG_FILE)
    app, api = web_application()
    resource_mapping(picking_system_mapper, api, app_params["endpoint_prefix"], myDB)
    app.run(ssl_context=app_params["ssl_context"], host=app_params["broadcastIp"], port=app_params["port"])

    # closing connection with MySQL
    myDB.close_connection()
