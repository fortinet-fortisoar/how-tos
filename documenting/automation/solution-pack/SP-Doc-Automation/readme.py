import logging
import os
from template import readme
from constants import *
from release_note import *


class Readme:

    def __init__(self, sp_dir_path, info_json_data):
        self.sp_dir_path = sp_dir_path
        self.info_json_data = info_json_data

    def create_readme_file_data(self):
        readme_file = self.__create_readme_file()
        logging.debug(
            "Successfully created \"{0}\" file".format(README_FILE_NAME))
        certified = 'No'
        if self.info_json_data.get('certified') and self.info_json_data.get('certified') == 'true':
            certified = 'Yes'
        compatible_version = self.info_json_data['fsrMinCompatibility'] + ' and later'

        # Check for new version
        release_note_content = ''
        if self.info_json_data['version'] != '1.0.0':
            release_note = ReleaseNote(self.sp_dir_path)
            release_note.create_release_note_file_data()
            release_note_content = ' * [Release Notes](./{0})'.format(
                RELEASE_NOTE_FILE_NAME)

        readme_file.write(readme.substitute(version=self.info_json_data['version'], certify=certified, publisher=self.info_json_data['publisher'],
                                            compatible_version=compatible_version, overview=self.info_json_data['description'], docs_name=DOC_FOLDER_NAME, release_note=release_note_content))
        readme_file.close()
        logging.debug(
            "Successfully written readme data in \"{0}\" file".format(README_FILE_NAME))

    def __create_readme_file(self):
        contents_file_path = os.path.join(self.sp_dir_path, README_FILE_NAME)
        return open(contents_file_path, 'w')
