import logging
import os
from template import *
from constants import *


class Contents:

    def __init__(self, sp_dir_path, sp_docs_path, sp_file_folder_list, info_json_data, outbreak_alert_data, threat_hunt_rules_data):
        self.sp_dir_path = sp_dir_path
        self.sp_docs_path = sp_docs_path
        self.sp_file_folder_list = sp_file_folder_list
        self.new_info_json_data = info_json_data
        self.outbreak_alert_data = outbreak_alert_data
        self.threat_hunt_rules_data = threat_hunt_rules_data
        
    def create_contents_file_data(self):
        contents_file = self.__create_contents_file()
        self.__create_contents_data(contents_file)

    # Create contents.md file
    def __create_contents_file(self):
        contents_file_path = os.path.join(
            self.sp_docs_path, CONTENTS_FILE_NAME)
        return open(contents_file_path, 'w')
    
    def _which_rule(self, picklist_value: str)-> str:
        if picklist_value == SIGMA_PICKLIST_VALUE:
            return "Sigma"
        
        elif picklist_value == YARA_PICKLIST_VALUE:
            return "Yara"
        
        elif picklist_value == FORTINET_FABRIC_PICKLIST_VALUE:
            return "Fortinet Fabric"

        else:
            raise Exception(f"Unknown Picklist Value of value {picklist_value}")

    def __create_contents_data(self, contents_file):
        threat_rules_content = ""
        for i in self.threat_hunt_rules_data:
            threat_rules_content += f"| {i['title']} | {self._which_rule(i['ruleType'])} |\n"
        
        contents_file.write(
            content.substitute(
                title=self.outbreak_alert_data['title'],
                description=self.outbreak_alert_data['description'],
                rules=threat_rules_content
            )
        )
        
        contents_file.close()
        logging.debug(f"Successfully written contents data in {CONTENTS_FILE_NAME} file")