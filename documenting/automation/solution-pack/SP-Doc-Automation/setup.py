import os
import json
import requests
import logging
from template import *
from constants import *
from logging import log


class Setup:

    def __init__(self, sp_dir_path, sp_docs_path, sp_folder_list, info_json_data):
        self.sp_dir_path = sp_dir_path
        self.sp_docs_path = sp_docs_path
        self.sp_folder_list = sp_folder_list
        self.info_json_data = info_json_data
        self.solution_name = self.info_json_data['label']

    def create_setup_file_data(self):
        setup_file = self.__create_setup_file()
        log(logging.DEBUG, "Successfully created {0} file".format(
            SETUP_FILE_NAME))
        self.__create_setup_data(setup_file)

    def __create_setup_file(self):
        setup_file_path = os.path.join(self.sp_docs_path, SETUP_FILE_NAME)
        return open(setup_file_path, 'w')

    def __create_setup_data(self, setup_file):

        # Dependencies Data
        dependencies_main_content = ''
        if 'dependencies' in self.info_json_data and len(self.info_json_data['dependencies']) > 0:
            dependencies_main_content = self.__create_dependencies_data()
            log(logging.DEBUG,
                "Successfully added dependencies data in {0} file".format(SETUP_FILE_NAME))

        # Connectors Data
        connectors_main_content = ''
        if 'connectors' in self.info_json_data['contents'] and len(self.info_json_data['contents']) > 0:
            connectors_main_content = self.__create_connector_data()
            log(logging.DEBUG,
                "Successfully added connectors data in {0} file".format(SETUP_FILE_NAME))

        setup_file.write(setup.substitute(readme_file=README_FILE_NAME, solution_name=self.solution_name,
                         prerequisites_data=dependencies_main_content, setup_connectors_data=connectors_main_content))
        setup_file.close()
        log(logging.DEBUG,
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
            log(logging.ERROR, "Solution Pack does not contains Connectors folder under path: {0}".format(
                self.sp_dir_path))
            return
        if 'data.json' not in os.listdir(self.sp_dir_path + '/connectors'):
            log(logging.ERROR,
                'Solution Pack does not contain data.json file under connector folder path: '.format(self.sp_dir_path + '/connectors'))
            return

        connector_doc_data = self.__get_fortisoar_connector_doc_data()
        log(logging.DEBUG, 'Successfully fetched Fortinet FortiSOAR doc link')
        connector_data_path = self.sp_dir_path + '/connectors/data.json'
        connectors_data_json = json.load(open(connector_data_path))
        for connector in connectors_data_json:
            connectors_content += setup_connectors_data.substitute(connector_name=connector['label'],
                                                                   connector_description=connector['description'], connector_doc_link='https://docs.fortinet.com/fortisoar/connectors/{0}'.format(self.__get_connector_doc_link(connector_doc_data, connector['label']))) + '\n'
        return connectors_content

    def __get_fortisoar_connector_doc_data(self):
        response = requests.get(FORTISOAR_CONNECTOR_DOC_LINK)
        return json.loads(response.text)

    def __get_connector_doc_link(self, connector_doc_data, connector_label):
        title_to_class = {item['title']: item['class']
                          for item in connector_doc_data.get('connectors')}
        if connector_label not in title_to_class.keys():
            log(logging.DEBUG,
                'Doc link for connector - \"{0}\" has not been found.'.format(connector_label))
            return ''
        doc_link = title_to_class.get(connector_label)
        log(logging.DEBUG,
            'Successfully fetched doc link for connector - \"{0}\"'.format(connector_label))
        return doc_link
