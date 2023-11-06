import logging
import os
import json
import requests
from template import *
from constants import *
import itertools


class Contents:

    def __init__(self, sp_dir_path, sp_docs_path, sp_file_folder_list, info_json_data, is_new_version, old_info_json_data, sp_repo_name, old_version_branch_name):
        self.sp_dir_path = sp_dir_path
        self.sp_docs_path = sp_docs_path
        self.sp_file_folder_list = sp_file_folder_list
        self.new_info_json_data = info_json_data
        self.is_new_version = is_new_version
        self.old_info_json_data = old_info_json_data
        self.sp_repo_name = sp_repo_name
        self.old_version_branch_name = old_version_branch_name

    def create_contents_file_data(self):
        contents_file = self.__create_contents_file()
        contents_key_list = self.__get_contents_key_list()
        self.__create_contents_data(contents_file, contents_key_list)

    def __create_contents_file(self):
        contents_file_path = os.path.join(
            self.sp_docs_path, CONTENTS_FILE_NAME)
        return open(contents_file_path, 'w')

    def __get_contents_key_list(self):
        contents_key_list = []
        for key, value in self.new_info_json_data['contents'].items():
            if value is not None:
                contents_key_list.append(key)
        return contents_key_list

    def __create_contents_data(self, contents_file, contents_key_list):

        # # dashboards
        dashboards_contents = ''
        if 'dashboards' in contents_key_list:
            dashboard_data = ''
            dashboard_data = self.__create_common_content_data('dashboards', True)
            dashboards_contents = dashboards_data.substitute(dashboards_sub_data=dashboard_data)
            logging.debug(f"Successfully fetched \"Dashboard\" data in {CONTENTS_FILE_NAME} file")

        # # picklist
        picklists_contents = ''
        if 'picklistNames' in contents_key_list:
            picklist_data = ''
            picklist_data = self.__create_common_content_data('picklistNames', False)
            picklists_contents = picklists_data.substitute(picklists_sub_data=picklist_data)
            logging.debug(f"Successfully fetched \"Picklist\" data in {CONTENTS_FILE_NAME} file")

        # # modules
        modules_contents = ''
        if 'modules' in contents_key_list:
            module_data = ''
            new_module_data = [self.new_info_json_data["contents"]["modules"][module]["name"] for module in self.new_info_json_data["contents"]["modules"].keys()]
            if self.is_new_version:
                old_module_data = [self.old_info_json_data["contents"]["modules"][module]["name"] for module in self.old_info_json_data["contents"]["modules"].keys()]
                diff_module_data = list(set(new_module_data) - set(old_module_data))
                module_data = self.__create_name_and_description_data(diff_module_data, True, module_data)
                module_data = self.__create_name_and_description_data(old_module_data, False, module_data)
            else:
                module_data = self.__create_name_and_description_data(new_module_data, False, module_data)
            modules_contents = modules_data.substitute(modules_sub_data=module_data)
            logging.debug(f"Successfully fetched \"Modules\" data in {CONTENTS_FILE_NAME} file")

        # # global variables
        global_variables_contents = ''
        if 'globalVariables' in contents_key_list:
            global_variable_data = ''
            global_variable_data = self.__create_common_content_data('globalVariables', True)
            global_variables_contents = global_variables_data.substitute(global_variables_sub_data=global_variable_data)
            logging.debug(f"Successfully fetched \"Global Variables\" data in {CONTENTS_FILE_NAME} file")

        # # roles
        roles_contents = ''
        if 'roles' in contents_key_list:
            role_data = ''
            role_data = self.__create_common_content_data('roles', True)
            roles_contents = roles_data.substitute(roles_sub_data=role_data)
            logging.debug(f"Successfully fetched \"Roles\" data in {CONTENTS_FILE_NAME} file")

        # # reports
        reports_contents = ''
        if 'reports' in contents_key_list:
            report_data = ''
            report_data = self.__create_common_content_data('reports', True)
            reports_contents = report_head.substitute(report_sub_data=report_data)
            logging.debug(f"Successfully fetched \"Reports\" data in {CONTENTS_FILE_NAME} file")

        # # record sets
        record_sets_contents = ''
        if 'recordSets' in contents_key_list:
            record_set_data = ''
            record_folder_list = os.listdir(self.sp_dir_path + '/records')
            new_record_set_data = [record["apiName"] for record in self.new_info_json_data["contents"]["recordSets"]]
            if self.is_new_version:
                old_record_set_data = [record["apiName"] for record in self.old_info_json_data["contents"]["recordSets"]]
                diff_record_set_data = list(set(new_record_set_data) - set(old_record_set_data))
                record_sets_json_path = self.__create_record_set_path_file(diff_record_set_data, record_folder_list)
                if len(record_sets_json_path) > 0:
                    record_set_data = self.__create_new_record_sets_data(record_sets_json_path, True, record_set_data)
                record_sets_json_path = self.__create_record_set_path_file(old_record_set_data, record_folder_list)
                if len(record_sets_json_path) > 0:
                    record_set_data = self.__create_record_sets_data(record_sets_json_path, record_set_data)
            else:
                record_sets_json_path = self.__create_record_set_path_file(new_record_set_data, record_folder_list)
                if len(record_sets_json_path) > 0:
                    record_set_data = self.__create_new_record_sets_data(record_sets_json_path, False, record_set_data)
            record_sets_contents = record_set_data
            logging.debug(f"Successfully fetched \"Record Sets\" data in {CONTENTS_FILE_NAME} file")

        # # connectors
        connectors_contents = ''
        if 'connectors' in contents_key_list:
            connector_data = ''
            if 'connectors' not in self.sp_file_folder_list:
                raise Exception(f'Connector folder not found under path: {self.sp_dir_path} yet connector listings were discovered in info.json of Solution Pack. Please export the Solution Pack once again.')
            if 'data.json' not in os.listdir(self.sp_dir_path + '/connectors'):
                raise Exception(f'\"data.json\" file was not found under path: {self.sp_dir_path}/connectors despite the connector lists in info.json and connector folder being in the solution pack. Please export the Solution Pack once again.')
            connector_data_json = json.load(open(self.sp_dir_path + '/connectors/data.json'))
            new_connector_data = [connector["apiName"] for connector in self.new_info_json_data["contents"]["connectors"]]
            if self.is_new_version:
                old_connector_data = [connector["apiName"] for connector in self.old_info_json_data["contents"]["connectors"]]
                diff_connector_data = list(set(new_connector_data) - set(old_connector_data))
                connector_data = self.__create_connectors_data(connector_data_json, diff_connector_data)
            else:
                connector_data = self.__create_connectors_data(connector_data_json, [])
            connectors_contents = connectors_data.substitute(connectors_sub_data=connector_data)
            logging.debug(f"Successfully fetched \"Connectors\" data in {CONTENTS_FILE_NAME} file")

        # # widgets
        widgets_contents = ''
        if 'widgets' in contents_key_list:
            widget_data = ''
            widget_data = self.__create_common_content_data('widgets', True)
            widgets_contents = widgets_data.substitute(widgets_sub_data=widget_data)
            logging.debug(f"Successfully fetched \"Widgets\" data in {CONTENTS_FILE_NAME} file")

        # # playbooks
        playbook_data = ''
        playbooks_contents = ''
        if 'playbooks' in contents_key_list:
            playbook_collection_folder_path = self.sp_dir_path + '/playbooks'
            playbook_collection_folder = os.listdir(playbook_collection_folder_path)
            new_playbook_collection_data = [playbook["name"] for playbook in self.new_info_json_data["contents"]["playbooks"]]
            if self.is_new_version:
                old_playbook_collection_data = [playbook["name"] for playbook in self.old_info_json_data["contents"]["playbooks"]]
                diff_playbook_collection_data = list(set(new_playbook_collection_data) - set(old_playbook_collection_data))
                if len(diff_playbook_collection_data) > 0:
                    for playbook_collection_name in diff_playbook_collection_data:
                        if playbook_collection_name not in playbook_collection_folder:
                            raise Exception(f"Playbook collection {playbook_collection_name} was found under info.json of solution pack's, but not found under solution's pack folder path: {playbook_collection_folder_path}. Please export the Solution Pack once again.")
                        playbook_data = self.__create_collection_playbook_data(playbook_collection_name, True, playbook_collection_folder_path, playbook_data)
                for playbook_collection_name in old_playbook_collection_data:
                    playbook_name_sub_data = ''
                    if playbook_collection_name not in playbook_collection_folder:
                        raise Exception(f"Playbook collection {playbook_collection_name} was found under info.json of solution pack's, but not found under solution's pack folder path: {playbook_collection_folder_path}. Please export the Solution Pack once again.")
                    response = requests.get(OLD_SP_PLAYBOOK_COLLECTION_DATA.format(sp_repo_name=self.sp_repo_name, playbook_collection_name=playbook_collection_name, branch_name=self.old_version_branch_name))
                    playbooks_name_old_data = [item['name'] for item in response.json() if 'name' in item]
                    playbooks_name_new_data = os.listdir(playbook_collection_folder_path + '/' + playbook_collection_name)
                    diff_playbooks_name_data = list(set(playbooks_name_new_data) - set(playbooks_name_old_data))
                    for playbook in diff_playbooks_name_data:
                        if playbook != 'collection.metadata.json':
                            playbook_name_sub_data += self.__create_playbook_new_data(playbook_collection_name, playbook, playbook_collection_folder_path, True)
                    for playbook in playbooks_name_old_data:
                        if playbook != 'collection.metadata.json':
                            playbook_name_sub_data += self.__create_playbook_new_data(playbook_collection_name, playbook, playbook_collection_folder_path, False)
                    playbook_data += playbooks_sub_data.substitute(name=playbook_collection_name, playbooks_sub_sub_data=playbook_name_sub_data)
            else:
                for playbook_collection_name in new_playbook_collection_data:
                    if playbook_collection_name not in playbook_collection_folder:
                        raise Exception(f"Playbook collection {playbook_collection_name} was found under info.json of solution pack's, but not found under solution's pack folder path: {playbook_collection_folder_path}. Please export the Solution Pack once again.")
                    playbook_name_sub_data = ''
                    playbooks_name_data = os.listdir(playbook_collection_folder_path + '/' + playbook_collection_name)
                    for playbook in playbooks_name_data:
                        if playbook != 'collection.metadata.json':
                            playbook_name_sub_data += self.__create_playbook_new_data(playbook_collection_name, playbook, playbook_collection_folder_path, False)
                    playbook_data += playbooks_sub_data.substitute(name=playbook_collection_name, playbooks_sub_sub_data=playbook_name_sub_data)
            playbooks_contents = playbooks_data.substitute(playbooks_sub_data=playbook_data)
            logging.debug(f"Successfully fetched \"Playbooks Collections and Playbook\" data in {CONTENTS_FILE_NAME} file")

        # # playbook blocks
        playbook_blocks_contents = ''
        if 'playbookBlocks' in contents_key_list:
            playbook_block_data = ''
            new_playbook_block_data = [playbookBlock["name"] for playbookBlock in self.new_info_json_data["contents"]["playbookBlocks"]]
            if self.is_new_version:
                old_playbook_block_data = [playbookBlock["name"] for playbookBlock in self.old_info_json_data["contents"]["playbookBlocks"]]
                diff_playbook_block_data = list(set(new_playbook_block_data) - set(old_playbook_block_data))
                playbook_block_data = self.__create_playbook_blocks_data(diff_playbook_block_data, True, playbook_block_data)
                playbook_block_data = self.__create_playbook_blocks_data(old_playbook_block_data, False, playbook_block_data)
            else:
                playbook_block_data = self.__create_playbook_blocks_data(new_playbook_block_data, False, playbook_block_data)
            playbook_blocks_contents = playbook_blocks_data.substitute(playbook_blocks_sub_data=playbook_block_data)
            logging.debug(f"Successfully fetched \"Playbook Blocks\" data in {CONTENTS_FILE_NAME} file")

        # # rules
        rules_content = ''
        if 'rules' in contents_key_list:
            rule_data = ''
            new_rule_data = [rule for rule in self.new_info_json_data["contents"]["rules"]]
            if self.is_new_version:
                old_rule_data = [rule for rule in self.old_info_json_data["contents"]["rules"]]
                diff_rule_data = list(set(new_rule_data) - set(old_rule_data))
                rule_data = self.__create_name_and_description_data(diff_rule_data, True, rule_data)
                rule_data = self.__create_name_and_description_data(old_rule_data, False, rule_data)
            else:
                rule_data = self.__create_name_and_description_data(new_rule_data, False, rule_data)
            rules_content = rules_data.substitute(rules_sub_data=rule_data)
            logging.debug(f"Successfully fetched \"Rules\" data in {CONTENTS_FILE_NAME} file")

        # # views
        views_content = ''
        if 'views' in contents_key_list:
            view_data = ''
            new_view_data = [view for view in self.new_info_json_data["contents"]["views"]["navigation"]]
            if self.is_new_version:
                old_view_data = [view for view in self.old_info_json_data["contents"]["views"]["navigation"]]
                diff_view_data = list(set(new_view_data) - set(old_view_data))
                view_data = self.__create_name_data(diff_view_data, True, view_data)
                view_data = self.__create_name_data(old_view_data, False, view_data)
            else:
                view_data = self.__create_name_data(new_view_data, False, view_data)
            views_content = navigations_data.substitute(navigations_sub_data=view_data)
            logging.debug(f"Successfully fetched \"Views\" data in {CONTENTS_FILE_NAME} file")

        solution_name = self.new_info_json_data['label']
        # writing in content.md file
        contents_file.write(content.substitute(readme_file=README_FILE_NAME, solution_name=solution_name, dashboards_data=dashboards_contents,
                                               picklists_data=picklists_contents, modules_data=modules_contents,
                                               connectors_data=connectors_contents, widgets_data=widgets_contents,
                                               playbooks_data=playbooks_contents, rules_data=rules_content,
                                               global_variables_data=global_variables_contents,
                                               roles_data=roles_contents,
                                               report_head=reports_contents, record_sets_data=record_sets_contents,
                                               navigations_data=views_content,
                                               playbook_blocks_data=playbook_blocks_contents))
        contents_file.close()
        logging.debug(f"Successfully written contents data in {CONTENTS_FILE_NAME} file")

    def __create_common_content_data(self, contents_key, to_add_only_name):
        content_data = ''
        new_content_data = [content["name"] for content in self.new_info_json_data["contents"][contents_key]]
        if not self.is_new_version:
            if to_add_only_name:
                content_data = self.__create_name_data(new_content_data, False, content_data)
            else:
                content_data = self.__create_name_and_description_data(new_content_data, False, content_data)
            return content_data
        old_content_data = [content["name"] for content in self.old_info_json_data["contents"][contents_key]]
        diff_content_data = list(set(new_content_data) - set(old_content_data))
        if to_add_only_name:
            content_data = self.__create_name_data(diff_content_data, True, content_data)
            content_data = self.__create_name_data(old_content_data, False, content_data)
        else:
            content_data = self.__create_name_and_description_data(diff_content_data, True, content_data)
            content_data = self.__create_name_and_description_data(old_content_data, False, content_data)
        return content_data

    def __create_name_and_description_data(self, data_list, new_version, content_data):
        for data in data_list:
            if new_version:
                data += ' <sup>New</sup>'
            content_data += name_description_data.substitute(name=data, description='') + '\n'
        return content_data

    def __create_name_data(self, data_list, new_version, content_data):
        for data in data_list:
            if new_version:
                data += ' <sup>New</sup>'
            content_data += name_data.substitute(name=data) + '\n'
        return content_data

    def __create_record_set_path_file(self, record_sets_data, record_folder_list):
        record_sets_json_path = []
        for record in record_sets_data:
            if record in EXCLUDE_RECORD_SETS:
                logging.debug(f"Skipped record {record} as script define.")
                continue
            if record not in record_folder_list:
                raise Exception(f"Record Set {record} was identified in the solution pack's info.json file, but the folder containing the records was not located under path {self.sp_dir_path + '/records'}. Please export the Solution Pack once again.")
            record_api_json_file = os.path.join(self.sp_dir_path + '/records' + '/' + record, record + '0001.json')
            if os.path.isfile(record_api_json_file):
                record_sets_json_path.append({'name': record, 'path': record_api_json_file})
        return record_sets_json_path

    def __create_new_record_sets_data(self, record_sets_json_path, new_version, content_data):
        content_sub_data = ''
        for record_data in record_sets_json_path:
            record_json_data = json.load(open(record_data['path']))
            for data in record_json_data:
                if data['@type'] == 'AssetResource':
                    if new_version:
                        data['type'] += ' <sup>New</sup>'
                    content_sub_data += record_sets_sub_data.substitute(data1=data['type'], data2=data['description']) + '\n'
                elif data['@type'] == 'Attachment':
                    if new_version:
                        data['name'] += ' <sup>New</sup>'
                    content_sub_data += record_sets_sub_data.substitute(data1=data['name'], data2=data['description']) + '\n'
                elif data['@type'] == 'Scenario':
                    if new_version:
                        data['title'] += ' <sup>New</sup>'
                    content_sub_data += record_sets_sub_data.substitute(data1=data['title'], data2='') + '\n'
                elif data['@type'] == 'OutbreakAlert':
                    if new_version:
                        data['title'] += ' <sup>New</sup>'
                    content_sub_data += record_sets_sub_data.substitute(data1=data['title'], data2='') + '\n'
                elif data['@type'] == 'ThreatHuntRule':
                    if new_version:
                        data['title'] += ' <sup>New</sup>'
                    content_sub_data += record_sets_sub_data.substitute(data1=data['title'], data2='') + '\n'
            content_data += record_sets_data.substitute(record_name=record_data['name'], record_sets_sub_data=content_sub_data) + '\n'
            content_sub_data = ''
        return content_data

    def __create_record_sets_data(self, record_sets_json_path, content_data):
        content_sub_data = ''
        for record_data in record_sets_json_path:
            record_data_url = 'https://raw.githubusercontent.com/fortinet-fortisoar/' + self.sp_repo_name + '/' + self.old_version_branch_name + '/records/' + record_data['name'] + '/' + record_data['name'] + '0001.json'
            old_record_data = json.loads(requests.get(url=record_data_url).text)
            new_record_data = json.load(open(record_data['path']))
            diff_record_data = list(itertools.filterfalse(lambda x: x in new_record_data, old_record_data)) + list(itertools.filterfalse(lambda x: x in old_record_data, new_record_data))
            if len(diff_record_data) > 0:
                for data in diff_record_data:
                    if data['@type'] == 'AssetResource':
                        data['type'] += ' <sup>New</sup>'
                        content_sub_data += record_sets_sub_data.substitute(data1=data['type'], data2=data['description']) + '\n'
                    elif data['@type'] == 'Attachment':
                        data['name'] += ' <sup>New</sup>'
                        content_sub_data += record_sets_sub_data.substitute(data1=data['name'], data2=data['description']) + '\n'
                    elif data['@type'] == 'Scenario':
                        data['title'] += ' <sup>New</sup>'
                        content_sub_data += record_sets_sub_data.substitute(data1=data['title'], data2='') + '\n'
            for data in old_record_data:
                if data['@type'] == 'AssetResource':
                    content_sub_data += record_sets_sub_data.substitute(data1=data['type'], data2=data['description']) + '\n'
                elif data['@type'] == 'Attachment':
                    content_sub_data += record_sets_sub_data.substitute(data1=data['name'], data2=data['description']) + '\n'
                elif data['@type'] == 'Scenario':
                    content_sub_data += record_sets_sub_data.substitute(data1=data['title'], data2='') + '\n'
            content_data += record_sets_data.substitute(record_name=record_data['name'], record_sets_sub_data=content_sub_data) + '\n'
            content_sub_data = ''
        return content_data

    def __create_connectors_data(self, connector_data_json, diff_connector_data):
        content_data = ''
        for connector in connector_data_json:
            if connector['label'] in diff_connector_data:
                connector['label'] += ' <sup>New</sup>' 
            content_data += connectors_sub_data.substitute(name=connector['label'], description=connector['description']) + '\n'
        return content_data

    def __create_collection_playbook_data(self, playbook_collection_name, new_version, playbook_collection_folder_path, content_data):
        content_sub_data = ''
        playbook_collection_name_folder = playbook_collection_folder_path + '/' + playbook_collection_name
        playbook_collection_folder = os.scandir(playbook_collection_name_folder)
        for file in playbook_collection_folder:
            if file != 'collection.metadata.json' and file.is_file():
                file_data = json.load(open(file))
                if new_version: 
                    file_data['name'] += ' <sup>New</sup>'
                content_sub_data += playbooks_sub_sub_data.substitute(name=file_data['name'], description=file_data['description']) + '\n'
        content_data += playbooks_sub_data.substitute(name=playbook_collection_name, playbooks_sub_sub_data=content_sub_data)
        return content_data

    def __create_playbook_new_data(self, playbook_collection_name, playbook_name, playbook_collection_folder_path, new_version):
        playbook_name_sub_data = ''
        playbook_name_file = playbook_collection_folder_path + '/' + playbook_collection_name + '/' + playbook_name
        playbook_name_file_data = open(playbook_name_file)
        playbook_description = json.load(playbook_name_file_data)
        if new_version:
            playbook_name += ' <sup>New</sup>'
        playbook_name_sub_data += playbooks_sub_sub_data.substitute(name=playbook_name, description=playbook_description['description']) + '\n'
        playbook_name_file_data.close()
        return playbook_name_sub_data
    
    def __create_playbooks_data(self):
        playbook_collection_folder_path = self.sp_dir_path + '/playbooks'
        content_sub_data = ''
        content_data = ''
        playbook_collection_folder = os.listdir(
            playbook_collection_folder_path)
        for playbook_collection in self.info_json_data['contents']['playbooks']:
            if playbook_collection['name'] not in playbook_collection_folder:
                raise Exception(
                    "Playbook collection \"{0}\" was found under info.json of solution pack's, but not found under solution's pack folder path: \"{1}\". Please export the Solution Pack once again.".format(playbook_collection['name'], playbook_collection_folder_path))
            for file in os.scandir(playbook_collection_folder_path + '/' + playbook_collection['name']):
                if file.name != 'collection.metadata.json' and file.is_file():
                    file_data = json.load(open(file))
                    content_sub_data += playbooks_sub_sub_data.substitute(
                        name=file_data['name'], description=file_data['description']) + '\n'
            content_data += playbooks_sub_data.substitute(name=playbook_collection['name'],
                                                          playbooks_sub_sub_data=content_sub_data)
            content_sub_data = ''
        return playbooks_data.substitute(playbooks_sub_data=content_data)

    def __create_playbook_blocks_data(self, playbook_block_data, new_version, content_data):
        playbook_block_folder = os.listdir(self.sp_dir_path + '/playbookBlocks')
        for playbook_block in playbook_block_data:
            if playbook_block + '.json' not in playbook_block_folder:
                raise Exception(f'Playbook block {playbook_block} was identified in info.json of Solution Pack, but is not available under path: {self.sp_dir_path}/playbookBlocks. Please export the Solution Pack once again.')
            playbook_block_file_data = json.load(open(self.sp_dir_path + '/playbookBlocks' + '/' + playbook_block + '.json'))
            if new_version:
                playbook_block += ' <sup>New</sup>'
            content_data += playbook_blocks_sub_data.substitute(name=playbook_block, description=playbook_block_file_data['description'].replace('\n', '')) + '\n'
        return content_data