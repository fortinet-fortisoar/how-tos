from contents import *
from readme import *
from usage import *
from setup import *
import zipfile
from release_note import *
import logging
import argparse


class SolutionPackDocsAutomation:

    def __init__(self, sp_path):
        self.sp_path = str(sp_path)

    def create_docs(self):
        try:
            if not os.path.exists(self.sp_path):
                raise Exception(
                    'Provided Solution Pack path \"{0}\" does not exists. Please provide proper path.'.format(self.sp_path))
            if os.path.isdir(self.sp_path):
                logging.debug(
                    'Provided Solution Pack path: \"{0}\" is a directory.'.format(self.sp_path))
                sp_dir_path = self.sp_path
            elif zipfile.is_zipfile(self.sp_path):
                logging.debug(
                    'Provided Solution Pack path: \"{0}\" is a zip file.'.format(self.sp_path))
                sp_dir_path = self.unzip_sp_zip_folder()
                logging.debug('Successfully unzip Solution Pack')
            else:
                raise Exception(
                    "Solution Pack should be either folder or zip.")

            sp_file_folder_list = os.listdir(sp_dir_path)
            if "info.json" not in sp_file_folder_list:
                raise Exception(
                    "Solution Pack does not contain 'info.json' file under path: \"{0}\". Please export the Solution Pack once again.".format(sp_dir_path))

            # Get info.json data
            info_json_data = self.get_info_json_data(sp_dir_path)
            logging.debug("Successfully read info.json file")

            # check provided path is Solution Pack or not:
            if info_json_data.get('type') != 'solutionpack':
                raise Exception(
                    "Provide folder path is not of Solution Pack type.")

            sp_docs_path, sp_docs_res_path = self.create_docs_folder(
                sp_dir_path)

            # Writing in Readme.md file
            readme = Readme(sp_dir_path, info_json_data)
            readme.create_readme_file_data()

            # Writing in Content.md file
            contents = Contents(
                sp_dir_path, sp_docs_path, sp_file_folder_list, info_json_data)
            contents.create_contents_file_data()

            # Writing in Setup.md file
            setup = Setup(sp_dir_path, sp_docs_path, sp_file_folder_list,
                          info_json_data)
            setup.create_setup_file_data()

            # Writing in Usage.md file
            usage = Usage(sp_dir_path, sp_docs_path,
                          info_json_data)
            usage.create_usage_file_data()

        except Exception as error:
            logging.exception(error)

    def unzip_sp_zip_folder(self):
        with zipfile.ZipFile(self.sp_path, 'r') as sp_unzip_path:
            sp_unzip_path.extractall(
                path=os.path.dirname(sp_unzip_path.filename))
            unzipped_folder_path = os.path.join(os.path.dirname(sp_unzip_path.filename),
                                                os.path.splitext(os.path.basename(self.sp_path))[0])
        return unzipped_folder_path
        # with ZipFile(self.sp_path, 'r') as zip_ref:
        #     # Extract all contents to the same directory as the zip file
        #     extract_path = os.path.dirname(zip_ref.filename)
        #     zip_ref.extractall(path=extract_path)
        #
        #     # Get the expected directory name
        #     base_name = os.path.splitext(os.path.basename(self.sp_path))[0]
        #     expected_dir_name = base_name.split(' ')[0]
        #     print('expected_dir_name ', expected_dir_name)
        #
        #     # Check if the expected directory exists
        #     extracted_dir = os.path.join(extract_path, expected_dir_name)
        #     if not os.path.exists(extracted_dir):
        #         # Rename the extracted directory to the expected name
        #         os.rename(os.path.join(extract_path, base_name), extracted_dir)
        #
        #     # Return the path of the renamed directory
        #     return extracted_dir

    # Get info.json file data
    def get_info_json_data(self, sp_dir_path):
        info_json_file_path = sp_dir_path + '/info.json'
        info_json_data = open(info_json_file_path)
        info_json = json.load(info_json_data)
        return info_json

    # create doc folder if not exists
    def create_docs_folder(self, sp_dir_path):
        sp_docs_path = os.path.join(sp_dir_path, DOC_FOLDER_NAME)
        sp_docs_res_path = os.path.join(sp_docs_path, RESOURCE_FOLDER_NAME)
        if not os.path.isdir(sp_docs_path):
            os.mkdir(sp_docs_path)
            logging.debug(
                "Successfully created \"{0}\" folder.".format(DOC_FOLDER_NAME))
        if not os.path.isdir(sp_docs_res_path):
            os.mkdir(sp_docs_res_path)
            logging.debug("Successfully created \"{0}\" folder under \"{1}\"".format(
                RESOURCE_FOLDER_NAME, DOC_FOLDER_NAME))
        return sp_docs_path, sp_docs_res_path


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--sp-path', nargs='+',
                        help='Path of Solution Pack', required=True)
    args = parser.parse_args()
    docs_obj = SolutionPackDocsAutomation(' '.join(args.sp_path))
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
