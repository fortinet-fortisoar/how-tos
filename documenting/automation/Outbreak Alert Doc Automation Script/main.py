from contents import *
from readme import *
from usage import *
from setup import *
from specs import Specs
import zipfile
import logging
import argparse
from urllib.parse import urlparse
import sys
import json


class SolutionPackDocsAutomation:

    def __init__(self, sp_dir_path,sp_specs):
        self.sp_dir_path = str(sp_dir_path)
        self.sp_specs = sp_specs

    def create_docs(self):
        try:
            sp_file_folder_list = os.listdir(self.sp_dir_path)
            if "info.json" not in sp_file_folder_list:
                raise Exception(
                    f"Solution Pack does not contain 'info.json' file under path: {self.sp_dir_path}. Please export the Solution Pack once again."
                )
            
            if "outbreak_alerts0001.json" not in os.listdir(f"{self.sp_dir_path}/records/outbreak_alerts"):
                raise Exception(
                    f"Solution Pack does not contain 'outbreak_alerts0001.json' file under path: {self.sp_dir_path}/records/outbreak_alerts. Please export the Solution Pack once again."
                )
                
            if "threat_hunt_rules0001.json" not in os.listdir(f"{self.sp_dir_path}/records/threat_hunt_rules"):
                raise Exception(
                    f"Solution Pack does not contain 'threat_hunt_rules0001.json' file under path: {self.sp_dir_path}/records/threat_hunt_rules. Please export the Solution Pack once again."
                )
            # Get info.json data
            info_json_data = self._get_info_json_data(self.sp_dir_path)
            logging.debug("Successfully read info.json file")
            
            # Read Outbreak Alert source data
            outbreak_alert_data = self._get_outbreak_alert_data(self.sp_dir_path).get('sourceData')[0]
            logging.debug(f"Successfully read outbreak_alerts001.json file")
            
            # Read Threat Hunt Rules source data
            threat_hunt_rules_data = self._get_threat_hunt_rules_data(self.sp_dir_path)
            logging.debug(f"Successfully read threat_hunt_rules001.json file")

            # check provided path is Solution Pack or not
            if info_json_data.get("type") != "solutionpack":
                raise Exception("Provide folder path is not of Solution Pack type.")

            # Check if docs folder and files exists or not
            sp_docs_path, sp_docs_res_path = self.create_docs_folder(self.sp_dir_path)

            # Writing in Readme.md file
            readme = Readme(self.sp_dir_path, info_json_data, outbreak_alert_data)
            readme.create_readme_file_data()

            contents = Contents(
                self.sp_dir_path,
                sp_docs_path,
                sp_file_folder_list,
                info_json_data,
                outbreak_alert_data,
                threat_hunt_rules_data
            )
            contents.create_contents_file_data()

            # Writing in Setup.md file
            setup = Setup(
                self.sp_dir_path, sp_docs_path, info_json_data, outbreak_alert_data, threat_hunt_rules_data
            )
            setup.create_setup_file_data()

            # Writing in Usage.md file
            usage = Usage(self.sp_dir_path, sp_docs_path, info_json_data,outbreak_alert_data,threat_hunt_rules_data)
            usage.create_usage_file_data()

            # Specs
            if self.sp_specs:
                specs = Specs(self.sp_dir_path, sp_docs_path, info_json_data,outbreak_alert_data,threat_hunt_rules_data)
                specs.create_specs_file_data()
            
            logging.debug(
                'Successfully created doc for Solution Pack "'
                + info_json_data["label"]
                + '" under provided path: {}'.format(self.sp_dir_path)
            )

        except Exception as error:
            logging.exception(error)
            sys.exit(1)

    # Get info.json file data
    def _get_info_json_data(self, sp_dir_path: str):
        info_json_file_path = sp_dir_path + "/info.json"
        info_json_data = open(info_json_file_path)
        info_json = json.load(info_json_data)
        info_json_data.close()
        return info_json

    # Get Outbreak Alert data
    def _get_outbreak_alert_data(self, sp_dir_path: str):
        outbreak_alert_file_path = sp_dir_path + "/records/outbreak_alerts/outbreak_alerts0001.json"
        outbreak_alert_data = open(outbreak_alert_file_path)
        outbreak_alert_json = json.load(outbreak_alert_data)
        outbreak_alert_data.close()
        return outbreak_alert_json[0]
    
    # Get Threat Hunt Rules data
    def _get_threat_hunt_rules_data(self, sp_dir_path: str):
        threat_hunt_rules_path = sp_dir_path + "/records/threat_hunt_rules/threat_hunt_rules0001.json"
        threat_hunt_rules_data = open(threat_hunt_rules_path)
        threat_hunt_rules_json = json.load(threat_hunt_rules_data)
        threat_hunt_rules_data.close()
        return threat_hunt_rules_json
    
    # create doc folder if not exists
    def create_docs_folder(self, sp_dir_path: str)-> tuple[str, str]:
        sp_docs_path = os.path.join(sp_dir_path, DOC_FOLDER_NAME)
        sp_docs_res_path = os.path.join(sp_docs_path, RESOURCE_FOLDER_NAME)
        for folder_path in [sp_docs_path, sp_docs_res_path]:
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
                logging.debug(f"Successfully created {folder_path} folder.")

        return sp_docs_path, sp_docs_res_path

# Get Solution Pack details
def _get_sp_details() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sp-path", nargs="+", help="Path of Solution Pack", required=True
    )
    parser.add_argument(
        "--sp-specs",
        help="Specify this tag, If you want to create Specs for this Solution Pack",
        required=False,
        action="store_true"
    )
    return parser.parse_args()


# validate argument data
def _is_argument_data_valid(args: argparse.Namespace) -> str:

    try:
        # Validate solution pack provided path
        sp_path = args.sp_path[0]
        logging.debug(f"Validating solution pack of Path: {sp_path}")
        sp_valid_path = _is_sp_path_valid(sp_path)
        if sp_valid_path[0]:
            sp_path = sp_valid_path[1]

        return sp_path
    except Exception as error:
        logging.exception(error)
        sys.exit(1)


def _is_sp_path_valid(sp_path: str) -> tuple[bool, str]:
    if not os.path.exists(sp_path):
        raise Exception(
            f"Provided Solution Pack path {sp_path} does not exists. Please provide proper path."
        )
    if os.path.isdir(sp_path):
        logging.debug(f"Provided Solution Pack path:{sp_path} is a directory.")
        return True, sp_path
    elif zipfile.is_zipfile(sp_path):
        logging.debug(f"Provided Solution Pack path: {sp_path} is a zip file.")
        # Unzip the Given zip file
        return True, unzip_zip_folder(sp_path)
    else:
        raise Exception(
            f' Not a directory: \'{sp_path}\'. Solution Pack must be either "folder" or "zip".'
        )


def unzip_zip_folder(sp_path: str) -> str:
    """Unzip a given zip file at a given path.

    Args:
        sp_path (str): Provide a path to the zip file.

    Returns:
        str: The final path to the extracted zip folder.
    """
    with zipfile.ZipFile(sp_path, "r") as unzip_path:
        # Setting the Directory Path of the zip file and Extracting the Zip file to the same directory
        directory_path = os.path.dirname(unzip_path.filename)
        unzip_path.extractall(path=directory_path)
        # Setting the final Folder Path without the .zip extension
        unzipped_folder_path = os.path.join(
            directory_path, os.path.splitext(os.path.basename(sp_path))[0]
        )

    logging.debug("Successfully Unzipped Solution Pack")
    return unzipped_folder_path


def create_log_file() -> None:
    """
    Creates a log file with path same as this script with name docs.log
    """
    log_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "docs.log")
    logging.basicConfig(
        level=logging.NOTSET,
        filename=log_filename,
        filemode="a",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create a Command line console logger
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_logger.setFormatter(console_formatter)

    # Get the root logger
    logger = logging.getLogger()
    logger.addHandler(console_logger)


if __name__ == "__main__":
    # Get the command line arguments for Solution Pack
    args = _get_sp_details()
    # Create Log files
    create_log_file()
    logging.debug(args)
    sp_dir_path = _is_argument_data_valid(args)

    docs_obj = SolutionPackDocsAutomation(sp_dir_path, args.sp_specs)
    docs_obj.create_docs()
