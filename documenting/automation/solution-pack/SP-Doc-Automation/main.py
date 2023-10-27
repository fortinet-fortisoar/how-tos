from contents import *
from readme import *
from usage import *
from setup import *
import zipfile
from release_note import *
import logging
import argparse
from urllib.parse import urlparse
import sys
from utils import *


class SolutionPackDocsAutomation:

    def __init__(self, sp_dir_path, sp_repo_name, old_version_branch_name, is_new_version):
        self.sp_dir_path = str(sp_dir_path)
        self.is_new_version = is_new_version
        self.sp_repo_name, self.old_version_branch_name = '', ''
        if sp_repo_name:
            self.sp_repo_name = sp_repo_name[0]
        if old_version_branch_name:
            self.old_version_branch_name = old_version_branch_name[0]

    def create_docs(self):
        try:
            sp_file_folder_list = os.listdir(self.sp_dir_path)
            if "info.json" not in sp_file_folder_list:
                raise Exception(f"Solution Pack does not contain 'info.json' file under path: {self.sp_dir_path}. Please export the Solution Pack once again.")

            # Get info.json data
            info_json_data = self.get_info_json_data(self.sp_dir_path)
            logging.debug("Successfully read info.json file")

            # check provided path is Solution Pack or not
            if info_json_data.get('type') != 'solutionpack':
                raise Exception("Provide folder path is not of Solution Pack type.")

            # Check if docs folder and files exists or not
            sp_docs_path, sp_docs_res_path = self.create_docs_folder(self.sp_dir_path)

            # Writing in Readme.md file
            readme = Readme(self.sp_dir_path, info_json_data,self.is_new_version)
            readme.create_readme_file_data()

            # # Writing in Content.md file
            old_info_json = ''
            if self.is_new_version:
                old_info_json = self.get_old_info_json_data()
            contents = Contents(self.sp_dir_path, sp_docs_path, sp_file_folder_list, info_json_data, self.is_new_version, old_info_json, self.sp_repo_name, self.old_version_branch_name)
            contents.create_contents_file_data()

            # Writing in Setup.md file
            setup = Setup(self.sp_dir_path, sp_docs_path, sp_file_folder_list, info_json_data)
            setup.create_setup_file_data()

            # Writing in Usage.md file
            if not self.is_new_version:
                usage = Usage(self.sp_dir_path, sp_docs_path, info_json_data)
                usage.create_usage_file_data()
            
            logging.debug('Successfully created doc for Solution Pack \"' + info_json_data['label'] + '\" under provided path: {}'.format(self.sp_dir_path))

        except Exception as error:
            logging.exception(error)
            sys.exit(1)

    # Get old info.json file data
    def get_old_info_json_data(self):
        response = requests.get(OLD_SP_INFO_JSON_DATA.format(sp_repo_name=self.sp_repo_name, branch_name=self.old_version_branch_name))
        info_json = json.loads(response.text)
        return info_json

    # Get info.json file data
    def get_info_json_data(self, sp_dir_path):
        info_json_file_path = sp_dir_path + '/info.json'
        info_json_data = open(info_json_file_path)
        info_json = json.load(info_json_data)
        info_json_data.close()
        return info_json

    # create doc folder if not exists
    def create_docs_folder(self, sp_dir_path):
        sp_docs_path = os.path.join(sp_dir_path, DOC_FOLDER_NAME)
        sp_docs_res_path = os.path.join(sp_docs_path, RESOURCE_FOLDER_NAME)
        for folder_path in [sp_docs_path, sp_docs_res_path]:
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
                logging.debug(f"Successfully created {folder_path} folder.")
        if self.is_new_version:
            self.download_and_create_md_files(OLD_SP_DOC_DATA.format(sp_repo_name=self.sp_repo_name, folder_to_copy='', branch_name=self.old_version_branch_name), sp_dir_path, False)
            self.download_and_create_md_files(OLD_SP_DOC_DATA.format(sp_repo_name=self.sp_repo_name, folder_to_copy='docs', branch_name=self.old_version_branch_name), sp_docs_path, False)
            self.download_and_create_md_files(OLD_SP_DOC_DATA.format(sp_repo_name=self.sp_repo_name, folder_to_copy='docs/res', branch_name=self.old_version_branch_name), sp_docs_res_path, True)
        return sp_docs_path, sp_docs_res_path

    def download_and_create_md_files(self, url, base_folder, is_res_folder):
        response = requests.get(url)

        if response.status_code == 200:
            contents = response.json()

            for item in contents:
                if item['type'] == 'file':
                    item_url = item['download_url']
                    file_name = os.path.join(base_folder, item['name'])

                    # Check if the file is an image (based on file extension)
                    if is_res_folder and item['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        file_content = requests.get(item_url).content
                        with open(file_name, 'wb') as file:
                            file.write(file_content)
                        logging.debug(f"Downloaded image: {file_name}")

                    # Check if the file is a markdown (.md) file
                    elif not is_res_folder and item['name'].endswith('.md'):
                        file_content = requests.get(item_url).text
                        with open(file_name, 'w', encoding='utf-8') as file:
                            file.write(file_content)
                        logging.debug(f"Downloaded and created: {file_name}")
        else:
            raise Exception(f"Failed to fetch contents from {url}. Status code: {response.status_code}")


# Get Solution Pack details
def get_sp_details():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sp-path', nargs='+', help='Path of Solution Pack', required=True)
    parser.add_argument('--sp-repo-name', nargs=1, help='Provide the github Solution Pack repo name', required=False)
    parser.add_argument('--old-version-branch-name', nargs=1, help='Provide the github old version branch name of Solution Pack', required=False)
    return parser.parse_args()

# validate argument data
def is_argument_data_valid(args):

    try:
        # validate solution pack provided path
        sp_path = ' '.join(args.sp_path)
        sp_valid_path = is_sp_path_valid(sp_path)
        if sp_valid_path[0]:
            sp_path = sp_valid_path[1]

        # validate repo name and branch name
        if args.sp_repo_name or args.old_version_branch_name:
            if args.sp_repo_name != None and args.old_version_branch_name == None:
                raise Exception(f'Solution Pack repository is specified as \"{args.sp_repo_name[0]}\", to create docs we requires the old version\'s branch name via the "--old-version-branch-name" argument.')
            if args.old_version_branch_name != None and args.sp_repo_name == None:
                raise Exception(f'Solution Pack old version\'s branch name is specified as \"{args.old_version_branch_name[0]}\", to create docs we requires the repository name via the "--sp-repo-name" argument.')
            if args.sp_repo_name or args.old_version_branch_name:
                response = requests.get(url=OLD_SP_INFO_JSON_DATA.format(sp_repo_name=args.sp_repo_name[0], branch_name=args.old_version_branch_name[0]))
                if response.status_code != 200:
                    raise Exception(f'Provided repository name: \"{args.sp_repo_name[0]}\", or branch name: \"{args.old_version_branch_name[0]}\" is incorrect.')
        return sp_path
    except Exception as error:
        logging.exception(error)
        sys.exit(1)

def is_sp_path_valid(sp_path):
    if not os.path.exists(sp_path):
        raise Exception(f'Provided Solution Pack path {sp_path} does not exists. Please provide proper path.')
    if os.path.isdir(sp_path):
        logging.debug(f'Provided Solution Pack path:{sp_path} is a directory.')
        return True, sp_path
    elif zipfile.is_zipfile(sp_path):
        logging.debug(f'Provided Solution Pack path: {sp_path} is a zip file.')
        utils = Utility(sp_path)
        return True, utils.unzip_zip_folder()
    else:
        raise Exception(f" Not a directory: \'{sp_path}\'. Solution Pack should be either \"folder\" or \"zip\".")


def create_log_file():
    log_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'docs.log')
    logging.basicConfig(level=logging.NOTSET, filename=log_filename, filemode='a',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a console logger
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_logger.setFormatter(console_formatter)

    # Get the root logger
    logger = logging.getLogger()
    logger.addHandler(console_logger)


if __name__ == "__main__":
    args = get_sp_details()
    create_log_file()
    is_new_version = False
    sp_dir_path = is_argument_data_valid(args)
    if args.sp_repo_name != None:
        is_new_version = True
    docs_obj = SolutionPackDocsAutomation(sp_dir_path, args.sp_repo_name, args.old_version_branch_name, is_new_version)
    docs_obj.create_docs()
