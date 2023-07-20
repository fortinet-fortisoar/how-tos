import os
import logging
from template import *
import json
from constants import *


class Setup:

    def __init__(self, widget_docs_path, info_json_data):
        self.widget_docs_path = widget_docs_path
        self.info_json_data = info_json_data
        self.widget_title = self.info_json_data['title']

    def create_setup_file_data(self):
        setup_file = self.__create_setup_file()
        logging.debug("Successfully created {0} file".format(SETUP_FILE_NAME))
        self.__create_setup_data(setup_file)

    def __create_setup_file(self):
        setup_file_path = os.path.join(self.widget_docs_path, SETUP_FILE_NAME)
        return open(setup_file_path, 'w')

    def __create_setup_data(self, setup_file):
        setup_file.write(setup.substitute(readme_file=README_FILE_NAME,
                                          widget_title=self.widget_title, usage_file=USAGE_FILE_NAME))
        setup_file.close()
        logging.debug(
            "Successfully written data in {0} file".format(SETUP_FILE_NAME))
