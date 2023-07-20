import os
import logging
from template import *
import json
from constants import *


class Setup:

    def __init__(self, sp_dir_path, sp_docs_path, sp_folder_list, info_json_data):
        self.sp_dir_path = sp_dir_path
        self.sp_docs_path = sp_docs_path
        self.sp_folder_list = sp_folder_list
        self.info_json_data = info_json_data
        self.solution_name = self.info_json_data['label']

    def create_setup_file_data(self):
        setup_file = self.__create_setup_file()
        logging.debug("Successfully created {0} file".format(SETUP_FILE_NAME))
        self.__create_setup_data(setup_file)

    def __create_setup_file(self):
        setup_file_path = os.path.join(self.sp_docs_path, SETUP_FILE_NAME)
        return open(setup_file_path, 'w')

    def __create_setup_data(self, setup_file):

        # Dependencies Data
        dependencies_main_content = ''
        if 'dependencies' in self.info_json_data and len(self.info_json_data['dependencies']) > 0:
            dependencies_main_content = self.__create_dependencies_data()
            logging.debug(
                "Successfully added dependencies data in {0} file".format(SETUP_FILE_NAME))

        # Connectors Data
        connectors_main_content = ''
        if 'connectors' in self.info_json_data['contents'] and len(self.info_json_data['contents']) > 0:
            connectors_main_content = self.__create_connector_data()
            logging.debug(
                "Successfully added connectors data in {0} file".format(SETUP_FILE_NAME))

        setup_file.write(setup.substitute(readme_file=README_FILE_NAME, solution_name=self.solution_name,
                         prerequisites_data=dependencies_main_content, setup_connectors_data=connectors_main_content))
        setup_file.close()
        logging.debug(
            "Successfully written data in {0} file".format(SETUP_FILE_NAME))

    def __create_dependencies_data(self):
        dependencies_content = ''
        for data in self.info_json_data['dependencies']:
            min_version = ''
            if data['minVersion']:
                min_version = data['minVersion'] + ' and later'
            dependencies_content += prerequisites_sub_data.substitute(
                spname=data['label'], version=min_version, purpose='') + '\n'
        return prerequisites_data.substitute(solution_name=self.solution_name, prerequisites_sub_data=dependencies_content)

    def __create_connector_data(self):
        connectors_content = ''
        if 'connectors' not in self.sp_folder_list:
            logging.error("Solution Pack does not contains Connectors folder under path: {0}".format(
                self.sp_dir_path))
            return
        if 'data.json' not in os.listdir(self.sp_dir_path + '/connectors'):
            logging.error(
                'Solution Pack does not contain data.json file under connector folder path: '.format(self.sp_dir_path + '/connectors'))
            return

        connector_data_path = self.sp_dir_path + '/connectors/data.json'
        connectors_data_json = json.load(open(connector_data_path))
        for connector in connectors_data_json:
            connectors_content += setup_connectors_data.substitute(connector_name=connector['label'],
                                                                   connector_description=connector['description'], connector_doc_link='https://docs.fortinet.com/fortisoar/connectors') + '\n'
        return connectors_content
