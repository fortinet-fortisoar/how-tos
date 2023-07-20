import logging
import os
import json
from template import *
from constants import *


class Contents:

    def __init__(self, sp_dir_path, sp_docs_path, sp_file_folder_list, info_json_data):
        self.sp_dir_path = sp_dir_path
        self.sp_docs_path = sp_docs_path
        self.sp_file_folder_list = sp_file_folder_list
        self.info_json_data = info_json_data

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
        for key, value in self.info_json_data['contents'].items():
            if value is not None:
                contents_key_list.append(key)
        return contents_key_list

    def __create_contents_data(self, contents_file, contents_key_list):

        # dashboards
        dashboards_contents = ''
        if 'dashboards' in contents_key_list:
            dashboards_contents = self.__create_dashboards_data()
            logging.debug(
                "Successfully added dashboard data in {0} file".format(CONTENTS_FILE_NAME))

        # picklist
        picklists_contents = ''
        if 'picklistNames' in contents_key_list:
            picklists_contents = self.__create_picklists_data()
            logging.debug(
                "Successfully added picklist data in {0} file".format(CONTENTS_FILE_NAME))

        # modules
        modules_contents = ''
        if 'modules' in contents_key_list:
            modules_contents = self.__create_modules_data()
            logging.debug(
                "Successfully added modules data in {0} file".format(CONTENTS_FILE_NAME))

        # global variables
        global_variables_contents = ''
        if 'globalVariables' in contents_key_list:
            global_variables_contents = self.__create_global_variables_data()
            logging.debug(
                "Successfully added global variables data in {0} file".format(CONTENTS_FILE_NAME))

        # roles
        roles_contents = ''
        if 'roles' in contents_key_list:
            roles_contents = self.__create_roles_data()
            logging.debug(
                "Successfully added roles data in {0} file".format(CONTENTS_FILE_NAME))

        # reports
        reports_contents = ''
        if 'reports' in contents_key_list:
            reports_contents = self.__create_reports_data()
            logging.debug(
                "Successfully added reports data in {0} file".format(CONTENTS_FILE_NAME))

        # record sets
        record_sets_contents = ''
        if 'recordSets' in contents_key_list:
            record_sets_contents = self.__create_record_sets_data()
            logging.debug(
                "Successfully added record sets data in {0} file".format(CONTENTS_FILE_NAME))

        # connectors
        connectors_contents = ''
        if 'connectors' in contents_key_list:
            connectors_contents = self.__create_connectors_data()
            logging.debug(
                "Successfully added connectors data in {0} file".format(CONTENTS_FILE_NAME))

        # widgets
        widgets_contents = ''
        if 'widgets' in contents_key_list:
            widgets_contents = self.__create_widgets_data()
            logging.debug(
                "Successfully added widgets data in {0} file".format(CONTENTS_FILE_NAME))

        # playbooks
        playbooks_contents = ''
        if 'playbooks' in contents_key_list:
            playbooks_contents = self.__create_playbooks_data()
            logging.debug(
                "Successfully added playbooks data in {0} file".format(CONTENTS_FILE_NAME))

        # playbook blocks
        playbook_blocks_contents = ''
        if 'playbookBlocks' in contents_key_list:
            playbook_blocks_contents = self.__create_playbook_blocks_data()
            logging.debug(
                "Successfully added playbook blocks data in {0} file".format(CONTENTS_FILE_NAME))

        # rules
        rules_content = ''
        if 'rules' in contents_key_list:
            rules_content = self.__create_rules_data()
            logging.debug(
                "Successfully added rules data in {0} file".format(CONTENTS_FILE_NAME))

        # views
        views_content = ''
        if 'views' in contents_key_list:
            views_content = self.__create_views_data()
            logging.debug(
                "Successfully added views data in {0} file".format(CONTENTS_FILE_NAME))

        solution_name = self.info_json_data['label']
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
        logging.debug(
            "Successfully written data in {0} file".format(CONTENTS_FILE_NAME))

    def __create_dashboards_data(self):
        content_data = ''
        for dashboard in self.info_json_data['contents']['dashboards']:
            content_data += dashboards_sub_data.substitute(
                name=dashboard['name'], description='') + '\n'
        return dashboards_data.substitute(dashboards_sub_data=content_data)

    def __create_picklists_data(self):
        content_data = ''
        for picklist in self.info_json_data['contents']['picklistNames']:
            content_data += picklists_sub_data.substitute(
                name=picklist['name']) + '\n'
        return picklists_data.substitute(picklists_sub_data=content_data)

    def __create_modules_data(self):
        content_data = ''
        for key in self.info_json_data['contents']['modules'].keys():
            content_data += modules_sub_data.substitute(
                name=self.info_json_data['contents']['modules'][key]['name'],
                description='') + '\n'
        return modules_data.substitute(modules_sub_data=content_data)

    def __create_global_variables_data(self):
        content_data = ''
        for global_variable in self.info_json_data['contents']['globalVariables']:
            content_data += global_variables_sub_data.substitute(
                name=global_variable['name'], description='') + '\n'
        return global_variables_data.substitute(global_variables_sub_data=content_data)

    def __create_roles_data(self):
        content_data = ''
        for role in self.info_json_data['contents']['roles']:
            content_data += roles_sub_data.substitute(
                name=role['name'], description='') + '\n'
        return roles_data.substitute(roles_sub_data=content_data)

    def __create_reports_data(self):
        content_data = ''
        for report in self.info_json_data['contents']['reports']:
            content_data += report_data.substitute(
                name=report['name'], description='') + '\n'
        return report_head.substitute(report_data=content_data)

    def __create_record_sets_data(self):
        content_sub_data = ''
        content_data = ''
        record_folder_list = os.listdir(self.sp_dir_path + '/records')
        record_sets_path = []

        for record in self.info_json_data['contents']['recordSets']:
            if record['apiName'] in EXCLUDE_RECORD_SETS:
                logging.debug(
                    "Skipped record {0} as script define.".format(record['apiName']))
                continue
            if record['apiName'] not in record_folder_list:
                logging.error(
                    "Solution Pack does not contains folder for record {0} under path {1}".format(record['apiName'], self.sp_dir_path + '/records'))
                continue
            record_api_json_file = os.path.join(
                self.sp_dir_path + '/records' + '/' + record['apiName'], record['apiName'] + '0001.json')
            if os.path.isfile(record_api_json_file):
                record_sets_path.append(
                    {'name': record['name'], 'path': record_api_json_file})
            else:
                logging.error(
                    "{0}0001.json file not found in records api folder".format(record['apiName']))

        for record_data in record_sets_path:
            record_json_data = json.load(open(record_data['path']))
            for data in record_json_data:
                if data['@type'] == 'AssetResource':
                    content_sub_data += record_sets_sub_data.substitute(data1=data['type'],
                                                                        data2=data['description']) + '\n'
                elif data['@type'] == 'Attachment':
                    content_sub_data += record_sets_sub_data.substitute(data1=data['name'],
                                                                        data2=data['description']) + '\n'
                elif data['@type'] == 'Scenario':
                    content_sub_data += record_sets_sub_data.substitute(
                        data1=data['title'], data2='') + '\n'
            content_data += record_sets_data.substitute(record_name=record_data['name'],
                                                        record_sets_sub_data=content_sub_data) + '\n'
            content_sub_data = ''
        return content_data

    def __create_connectors_data(self):
        content_data = ''
        if 'connectors' not in self.sp_file_folder_list:
            logging.error('Solution Pack does not contains Connectors folder under path: {0}'.format(
                self.sp_dir_path))
            return
        if 'data.json' not in os.listdir(self.sp_dir_path + '/connectors'):
            logging.error(
                'Solution Pack does not contain data.json file under Connectors folder path: {0}'.format(self.sp_dir_path + '/connectors'))
            return
        connector_data_path = self.sp_dir_path + '/connectors/data.json'
        connector_data_json = json.load(open(connector_data_path))

        for connector in connector_data_json:
            content_data += connectors_sub_data.substitute(name=connector['label'],
                                                           description=connector['description']) + '\n'
        return connectors_data.substitute(connectors_sub_data=content_data)

    def __create_widgets_data(self):
        content_data = ''
        for widget in self.info_json_data['contents']['widgets']:
            content_data += widgets_sub_data.substitute(
                name=widget.get('name'), description='') + '\n'
        return widgets_data.substitute(widgets_sub_data=content_data)

    def __create_playbooks_data(self):
        playbook_collection_folder_path = self.sp_dir_path + '/playbooks'
        content_sub_data = ''
        content_data = ''
        playbook_collection_folder = os.listdir(
            playbook_collection_folder_path)
        for playbook_collection in self.info_json_data['contents']['playbooks']:
            if playbook_collection['name'] not in playbook_collection_folder:
                logging.error(
                    'Solution Pack does not contain {0} file under playbooks collection folder path: {1}'.format(playbook_collection['name'], playbook_collection_folder_path))
                return
            for file in os.scandir(playbook_collection_folder_path + '/' + playbook_collection['name']):
                if file.name != 'collection.metadata.json' and file.is_file():
                    file_data = json.load(open(file))
                    content_sub_data += playbooks_sub_sub_data.substitute(
                        name=file_data['name'], description=file_data['description']) + '\n'
            content_data += playbooks_sub_data.substitute(name=playbook_collection['name'],
                                                          playbooks_sub_sub_data=content_sub_data)
            content_sub_data = ''
        return playbooks_data.substitute(playbooks_sub_data=content_data)

    def __create_playbook_blocks_data(self):
        playbook_block_folder_path = self.sp_dir_path + '/playbookBlocks'
        content_data = ''
        playbook_block_folder = os.listdir(playbook_block_folder_path)
        for playbook_block in self.info_json_data['contents']['playbookBlocks']:
            if playbook_block['name'] + '.json' not in playbook_block_folder_path:
                logging.error(
                    'Solution Pack does not contain {0} file under playbooks block folder path: {1}'.format(playbook_block['name'], playbook_block_folder_path))
                return
            playbook_block_file_data = json.load(
                open(playbook_block_folder_path + '/' + playbook_block['name'] + '.json'))
            content_data += playbook_blocks_sub_data.substitute(name=playbook_block_file_data['name'],
                                                                description=playbook_block_file_data['description'].replace('\n', '')) + '\n'
        return playbook_blocks_data.substitute(playbook_blocks_sub_data=content_data)

    def __create_rules_data(self):
        content_data = ''
        for rule in self.info_json_data['contents']['rules']:
            content_data += rules_sub_data.substitute(
                name=rule, description='') + '\n'
        return rules_data.substitute(rules_sub_data=content_data)

    def __create_views_data(self):
        content_data = ''
        for navigation in self.info_json_data['contents']['views']['navigation']:
            content_data += navigations_sub_data.substitute(
                name=navigation) + '\n'
        return navigations_data.substitute(navigations_sub_data=content_data)
