import os
import json
import requests
import logging
from template import *
from constants import *


class Setup:

    def __init__(self, sp_dir_path, sp_docs_path, info_json_data, outbreak_alert_data, threat_hunt_rules_data):
        self.sp_dir_path = sp_dir_path
        self.sp_docs_path = sp_docs_path
        self.info_json_data = info_json_data
        self.outbreak_alert_data = outbreak_alert_data
        self.threat_hunt_rules_data = threat_hunt_rules_data

    def create_setup_file_data(self):
        setup_file = self.__create_setup_file()
        logging.debug(
            "Successfully created \"{0}\" file".format(SETUP_FILE_NAME))
        self.__create_setup_data(setup_file)

    def __create_setup_file(self):
        setup_file_path = os.path.join(self.sp_docs_path, SETUP_FILE_NAME)
        return open(setup_file_path, 'w')

    def __create_setup_data(self, setup_file):
        setup_file.write(
            setup.substitute(title=self.outbreak_alert_data['title'])
        )
        setup_file.close()
        logging.debug(
            "Successfully written data in \"{0}\" file".format(SETUP_FILE_NAME))