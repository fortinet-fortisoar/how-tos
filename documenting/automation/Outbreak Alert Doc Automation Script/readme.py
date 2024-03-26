import logging
import os
from template import readme, version_data, certified_data, compatible_version_data,overview_data
from constants import *


class Readme:

    def __init__(self, sp_dir_path, info_json_data, outbreak_alert_data):
        self.sp_dir_path = sp_dir_path
        self.info_json_data = info_json_data
        self.outbreak_alert_data = outbreak_alert_data

    def create_readme_file_data(self) -> None:

        # Check for version
        version_content = version_data.substitute(
            version=self.info_json_data["version"]
        )

        # Check for Certification
        CERTIFIED = "No"
        if (self.info_json_data.get("certified") and self.info_json_data.get("certified") == "true"):
            CERTIFIED = "Yes"
        certified_content = certified_data.substitute(certify=CERTIFIED)

        # Check for Compatibility
        compatible_version_content = compatible_version_data.substitute(
            compatible_version=self.info_json_data["fsrMinCompatibility"] + " and later"
        )

        overview_content = overview_data.substitute(overview=self.outbreak_alert_data["description"], title=self.outbreak_alert_data["title"],link=self.outbreak_alert_data["link"])
    
        readme_file = self.__create_readme_file()
        logging.debug(f"Successfully created {README_FILE_NAME} file")
        readme_file.write(
            readme.substitute(
                version_data=version_content,
                certified_data=certified_content,
                publisher=self.info_json_data["publisher"],
                compatible_version_data=compatible_version_content,
                overview=overview_content,
                docs_name=DOC_FOLDER_NAME,
                background=self.outbreak_alert_data["background"],
                announced=self.outbreak_alert_data["announced"],
                latest=self.outbreak_alert_data["latest"]
            )
        )
        readme_file.close()

        logging.debug(f"Successfully written readme data in {README_FILE_NAME} file")

    def __create_readme_file(self):
        contents_file_path = os.path.join(self.sp_dir_path, README_FILE_NAME)
        return open(contents_file_path, "w")
