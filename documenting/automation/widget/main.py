from readme import *
from usage import *
from setup import *
from constants import *
import tarfile
import logging
import json
import os
import shutil
import argparse


class WidgetDocsAutomation:

    def __init__(self, widget_path):
        self.widget_path = str(widget_path)

    def create_docs(self):
        try:
            if not os.path.exists(self.widget_path):
                raise Exception(
                    'Provided widget path {0} does not exists.'.format(self.widget_path))
            if os.path.isdir(self.widget_path):
                logging.debug("Provided widget path {0} is directory.".format(
                    self.widget_path))
                widget_dir_path = ''
                if self.is_info_json_exists(self.widget_path):
                    widget_dir_path = self.restructure_widget_directory()
                    logging.debug(
                        'Successfully restructure widget directory folder.')
                else:
                    return
            elif tarfile.is_tarfile(self.widget_path):
                logging.debug("Provided widget path {0} is in tgz format.".format(
                    self.widget_path))
                widget_dir_path = self.uncompress_widget_tgz_folder()
                logging.debug('Successfully unzip widget tgz folder')
                if self.is_info_json_exists(widget_dir_path):
                    pass
                else:
                    return
            else:
                raise Exception(
                    "Widget should be either folder or tgz.")

            # Read info.json file
            info_json_data = self.get_info_json_data(widget_dir_path)
            logging.debug("Successfully read info.json file")

            # Create docs and res folder
            widget_docs_path, widget_docs_res_path = self.create_docs_folder(
                os.path.dirname(widget_dir_path))

            # Writing in Readme.md file
            readme = Readme(widget_dir_path, info_json_data)
            readme.create_readme_file_data()

            # Writing in Setup.md file
            setup = Setup(widget_docs_path, info_json_data)
            setup.create_setup_file_data()

            # Writing in Usage.md file
            usage = Usage(widget_docs_path, info_json_data)
            usage.create_usage_file_data()

        except Exception as error:
            logging.exception(error)
            raise Exception(error)

    # def is_path_exists(self):
    #     return os.path.exists()

    def is_info_json_exists(self, widget_dir_path):
        widget_file_folder_list = os.listdir(widget_dir_path)
        if "info.json" not in widget_file_folder_list:
            logging.error(
                "Widget does not contain info.json file under path: {0}".format(widget_dir_path))
            return False
        return True

    def uncompress_widget_tgz_folder(self):
        widget_file = tarfile.open(self.widget_path)
        widget_uncompress_folder = os.path.splitext(
            os.path.basename(widget_file.name))[0]
        widget_uncompress_path = os.path.join(os.path.dirname(
            widget_file.name), '{0}/{1}'.format(widget_uncompress_folder, WIDGET_FOLDER_NAME))
        with tarfile.open(self.widget_path, "r:gz") as tar:
            # Extract each file to the destination folder
            for member in tar.getmembers():
                # Remove the top-level folder from the member name
                member.name = os.path.relpath(
                    member.name, widget_uncompress_folder)
                # Calculate the destination path based on the adjusted member name
                dest_path = os.path.join(widget_uncompress_path, member.name)
                # Ensure that the directory structure exists before extracting
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                # Extract the file to the destination path
                tar.extract(member, path=widget_uncompress_path)
        return widget_uncompress_path

    # move all .html and .js files to 'widget' folder
    def restructure_widget_directory(self):
        allfiles = os.listdir(self.widget_path)
        widget_folder_path = os.path.join(self.widget_path, WIDGET_FOLDER_NAME)
        for file in allfiles:
            src_path = os.path.join(self.widget_path, file)
            dst_path = os.path.join(widget_folder_path, file)
            shutil.move(src_path, dst_path)
        return widget_folder_path

    # Get info.json file data
    def get_info_json_data(self, widget_dir_path):
        info_json_file_path = widget_dir_path + '/info.json'
        info_json_data = open(info_json_file_path)
        info_json = json.load(info_json_data)
        return info_json

    # create doc folder if not exists
    def create_docs_folder(self, widget_dir_path):
        widget_docs_path = os.path.join(widget_dir_path, DOC_FOLDER_NAME)
        widget_docs_res_path = os.path.join(
            widget_docs_path, RESOURCE_FOLDER_NAME)
        if not os.path.isdir(widget_docs_path):
            os.mkdir(widget_docs_path)
            logging.debug(
                "Successfully created {0} folder".format(DOC_FOLDER_NAME))
        if not os.path.isdir(widget_docs_res_path):
            os.mkdir(widget_docs_res_path)
            logging.debug("Successfully created {0} folder under {1}".format(
                RESOURCE_FOLDER_NAME, DOC_FOLDER_NAME))
        return widget_docs_path, widget_docs_res_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--widget-path', nargs='+',
                        help='Path of Widget', required=True)
    args = parser.parse_args()
    docs_obj = WidgetDocsAutomation(' '.join(args.widget_path))
    docs_obj.create_docs()


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, filename='docs.log', filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a console logger
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s")
    console_logger.setFormatter(console_formatter)

    # Get the root logger
    logger = logging.getLogger()
    logger.addHandler(console_logger)
    main()
