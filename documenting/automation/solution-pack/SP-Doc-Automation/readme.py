import logging
import os
from template import readme, version_data, certified_data, compatible_version_data
from constants import *
from release_note import *


class Readme:

    def __init__(self, sp_dir_path, info_json_data, is_new_version):
        self.sp_dir_path = sp_dir_path
        self.info_json_data = info_json_data
        self.is_new_version = is_new_version

    def create_readme_file_data(self):

        # Check for version
        version_content = version_data.substitute(version=self.info_json_data['version'])

        # Check for Certification
        certified = 'No'
        if self.info_json_data.get('certified') and self.info_json_data.get('certified') == 'true':
            certified = 'Yes'
        certified_content = certified_data.substitute(
            certify=certified)

        # Check for Compatibility
        compatible_version_content = compatible_version_data.substitute(
            compatible_version=self.info_json_data['fsrMinCompatibility'] + ' and later')

        release_note_content = ''

        if not self.is_new_version:
            readme_file = self.__create_readme_file()
            logging.debug(f"Successfully created {README_FILE_NAME} file")
            readme_file.write(readme.substitute(version_data=version_content, certified_data=certified_content, publisher=self.info_json_data['publisher'], compatible_version_data=compatible_version_content, overview=self.info_json_data['description'], docs_name=DOC_FOLDER_NAME, release_note=release_note_content))
            readme_file.close()
        else:
            with open(self.sp_dir_path + '/' + README_FILE_NAME, 'r') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if 'version' in line.lower():
                        lines[i] = version_content + '\n'
                    if 'certified' in line.lower():
                        lines[i] = certified_content + '\n'
                    if 'compatible version' in line.lower():
                        lines[i] = compatible_version_content + '\n'
                        break
            # Write the modified content back to the file
            with open(self.sp_dir_path + '/' + README_FILE_NAME, 'w') as file:
                file.writelines(lines)

        # Check for new version
        # if self.info_json_data['version'] != '1.0.0':
        #     release_note = ReleaseNote(self.sp_dir_path)
        #     release_note.create_release_note_file_data()
        #     release_note_content = ' * [Release Notes](./{0})'.format(
        #         RELEASE_NOTE_FILE_NAME)

        logging.debug(f"Successfully written readme data in {README_FILE_NAME} file")

    def __create_readme_file(self):
        contents_file_path = os.path.join(self.sp_dir_path, README_FILE_NAME)
        return open(contents_file_path, 'w')
