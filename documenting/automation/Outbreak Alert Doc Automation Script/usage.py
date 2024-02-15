import os
import logging
from template import *
from constants import *


class Usage:

    def __init__(self, sp_dir_path, sp_docs_path, info_json_data, outbreak_alert_data, threat_hunt_rules_data):
        self.sp_dir_path = sp_dir_path
        self.sp_docs_path = sp_docs_path
        self.info_json_data = info_json_data
        self.outbreak_alert_data = outbreak_alert_data
        self.threat_hunt_rules_data = threat_hunt_rules_data

    def create_usage_file_data(self):
        usage_file = self.__create_usage_file()
        logging.debug(
            "Successfully created \"{0}\" file".format(USAGE_FILE_NAME))
        self.__create_usage_data(usage_file)

    def __create_usage_file(self):
        usage_file_path = os.path.join(self.sp_docs_path, USAGE_FILE_NAME)
        return open(usage_file_path, 'w')

    def __create_usage_data(self, usage_file):
        usage_file.write(usage.substitute(title=self.outbreak_alert_data['title']))
        usage_file.close()
        logging.debug(
            "Successfully written data in \"{0}\" file".format(USAGE_FILE_NAME))
