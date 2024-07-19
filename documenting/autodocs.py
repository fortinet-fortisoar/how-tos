""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import json
import os
import re
import sys
import markdown2
from operator import itemgetter

operators = {
    '===': 'as',
    '!==': 'is not equal to',
    '': 'is not specified'
}

logical_operators = {
    '&&': 'and',
    '||': 'or'
}

def write_onchange_param(md_file_fp, param):
    onchange_config_params = param['onchange']
    for on_param in onchange_config_params:
        md_file_fp.write("<strong>If you choose '{param}'</strong>".format(param=on_param))
        temp_param_list = onchange_config_params[on_param]
        md_file_fp.write("<ul>")
        for item in temp_param_list:
            md_file_fp.write("<li>{title}: {desc}</li>".format(title=item['title'], desc=item.get('description', '')))
            if "onchange" in item:
                write_onchange_param(md_file_fp, item)
        md_file_fp.write("</ul>")


def write_output_schema(output_schema):
    # Removed <code><br>&nbsp;</code> and used <pre> tag instead.
    if type(output_schema) is dict or type(output_schema) is list:
        output_schema = json.dumps(output_schema, indent=4, sort_keys=False)
        md_file_fp.write("\n<pre>{0}</pre>\n".format(output_schema))
    else:
        md_file_fp.write("\n")
        md_file_fp.write("The output contains a non-dictionary value.\n")


def find_param_title(parameters, name):
    for param in parameters:
        if param['name'] == name:
            return param['title']
    return ''


def get_file_full_path(info_file_path, filename):
    full_path = os.path.split(info_file_path)
    if full_path:
        dir_path = full_path[0]
        if os.path.exists(dir_path):
            release_notes_file_path = os.path.join(dir_path, filename)
            if os.path.isfile(release_notes_file_path):
                return release_notes_file_path
            else:
                return None


def adding_release_notes(info_file_path, md_file_fp, display_name, version):
    release_notes_file_path =  get_file_full_path(info_file_path, 'release_notes.md')
    if release_notes_file_path:
        md_file_fp.write("## Release Notes for version {version}\n".format(version=version))
        md_file_fp.write(
            "Following enhancements have been made to the {connector_name} Connector in version {version}:\n".format(
                connector_name=display_name, version=version))
        with open(release_notes_file_path, 'r') as f:
            release_note_text = f.read()
            list_release_notes = release_note_text.splitlines()
            for line in list_release_notes:
                if re.search('####', line):
                    list_release_notes.pop(list_release_notes.index(line))
            release_note_text = '\n\n'.join(list_release_notes)
            html = markdown2.markdown(release_note_text)
            html = re.sub(r'<li><p>(.*?)</p></li>', r'<li>\1</li>', html)  # to remove unnecessary <p></p> tags from <li></li> tags
            md_file_fp.write(html)


def add_about_connector_content(md_file_fp, display_name):
    md_file_fp.write("## About the connector\n")
    md_file_fp.write(description)
    md_file_fp.write("\n")
    md_file_fp.write(
        "<p>This document provides information about the {connector_name} Connector, which facilitates automated interactions, with a {connector_name} server using FortiSOAR&trade; playbooks. Add the {connector_name} Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with {connector_name}.</p>".format(
            connector_name=display_name))
    md_file_fp.write("\n")


def add_version_info(md_file_fp, display_name, version, publisher, approved):
    md_file_fp.write("\n### Version information\n")
    md_file_fp.write("\n")
    md_file_fp.write("Connector Version: {version}\n".format(version=version))
    md_file_fp.write("\n")
    if approved:
        md_file_fp.write("FortiSOAR&trade; Version Tested on: 7.4.1-3167\n")
        md_file_fp.write("\n")
        md_file_fp.write("{0} Version Tested on: {1}\n".format(display_name, vendor_version))
    md_file_fp.write("\n")
    md_file_fp.write("Authored By: {0}\n".format(publisher))
    md_file_fp.write("\n")
    if approved:
        md_file_fp.write("Certified: Yes\n")
    else:
        md_file_fp.write("Certified: No\n")


def add_installing_connector_content(md_file_fp, connector_name):
    md_file_fp.write("\n## Installing the connector\n")
    md_file_fp.write(
        "<p>Use the <strong>Content Hub</strong> to install the connector. For "
        "the detailed procedure to install a connector, "
        "click <a href=\"https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector\" "
        "target=\"_top\">here</a>.</p><p>You can also use the <code>yum</code> command as a root user to install the connector:</p>")
    md_file_fp.write("\n")
    md_file_fp.write("<pre>yum install cyops-connector-{name}</pre>\n".format(name=connector_name))
    md_file_fp.write("\n")


def add_prerequisites_content(md_file_fp, display_name):
    md_file_fp.write("## Prerequisites to configuring the connector\n")
    if config:
        md_file_fp.write(
            "- You must have the credentials of {0} server to which you will connect and perform automated operations.\n".format(display_name))
        md_file_fp.write("- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the {connector_name} server.".format(connector_name=display_name)
                         )
        md_file_fp.write("\n")
    else:
        md_file_fp.write("There are no prerequisites to configuring this connector.\n")

def add_minimum_permission_section(md_file_fp):
    md_file_fp.write("\n")
    md_file_fp.write("## Minimum Permissions Required\n")
    md_file_fp.write("- Not applicable\n")

def add_configuration_parameters(md_file_fp, display_name, config):
    md_file_fp.write("\n")
    md_file_fp.write("## Configuring the connector\n")
    md_file_fp.write(
        "For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)")
    md_file_fp.write("\n")
    md_file_fp.write("### Configuration parameters\n")
    if config:
        md_file_fp.write(
            "<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>{connector_name}</strong> connector row "
            "(if you are in the <strong>Grid</strong> view on the Connectors page) and in the"
            " <strong>Configurations</strong>"
            " tab enter the required configuration details:</p>\n".format(connector_name=display_name))
        md_file_fp.write("<table border=1>")
        md_file_fp.write("<thead>")
        md_file_fp.write("<tr>")
        md_file_fp.write("<th>Parameter</th>")
        md_file_fp.write("<th>Description</th>")
        md_file_fp.write("</tr>")
        md_file_fp.write("</thead>")
        md_file_fp.write("<tbody>")
    else:
        md_file_fp.write("None.\n")
    for param in config.get('fields', []):
        if param['title'] == 'Verify SSL':
            md_file_fp.write("<tr><td>{0}</td>"
                             "<td>{1}</td></tr>\n".format(param['title'],
                                                              "Specifies whether the SSL certificate for the server is "
                                                              "to be verified or not. <br/>By default, "
                                                              "this option is set to True."))
        else:
            if not (param.get('visible', True) is False or param.get('enabled', True) is False):
                md_file_fp.write("<tr><td>{0}</td>"
                                 "<td>{1}\n".format(param['title'], param.get('description', '')))
            if "onchange" in param:
                md_file_fp.write("<br>")
                write_onchange_param(md_file_fp, param)
            md_file_fp.write("</td>\n</tr>")  # closing the <td> and <tr> tags.
    md_file_fp.write("</tbody>")
    md_file_fp.write("</table>")
    md_file_fp.write("\n")


def parse_condition(condition):
    if condition.startswith("this"):
        condition = condition.split()
    else:
        condition = condition.split("'") if "'" in condition else condition.split()
    if isinstance(condition, list) and len(condition) > 3:
            operand1 = condition[0]
            operator = condition[1]
            operand2 = " ".join(condition[2:]).replace('\'', '')
    elif isinstance(condition, list) and len(condition) == 3:
        if condition[0].startswith("this") or condition[2] in ['true', 'false']:
            operand1 = condition[0]
            operand1 = operand1.split("'")[1] if "'" in operand1 else condition[0]
            operator = condition[1]
            operand2 = condition[2].replace('\'', '')
        else:
            con1 = condition[0].split(' ')
            if isinstance(con1, list):
                operand1 = con1[0]
                operator = con1[1]
            operand2 = condition[1].replace('\'', '')
    return operand1, operator, operand2

def create_message_content(operand2, title, operator):
    msg = '\"{}\"'.format(operand2) if operand2 not in operators else operators.get(operand2)
    msg_content = f'\nOutput schema {"when you choose" if operand2 else "when the"} "{title}" {operators.get(operator, "") if operand2 else ""} {msg}:'
    return msg_content


def extract_multiple_condition(condition, opr, action_parameters):
    try:
        condition=condition.replace('(','').replace(')','')
        condition = condition.split(opr)
        msg_content=''
        list_condition = [cond.strip() for cond in condition]
        if condition and isinstance(condition, list) and len(condition)>=2:
            operand1, operator, operand2 = parse_condition(list_condition[0])
            title1 = find_param_title(action_parameters, operand1)
            operand_1, operator_, operand_2 = parse_condition(list_condition[1])
            title2 = find_param_title(action_parameters, operand_1)

            if title1 == title2 and operand_2 and operand2:
                msg_content=f'If you choose "{operand2}" {logical_operators.get(opr)} "{operand_2}" as the "{title1}", then the output contains the following populated JSON schema:\n'

            # {{domain !== '' && emailAddress === 'some value'}}
            elif title1 != title2 and operand_2 and operand2:
                msg_content= f'If you choose "{title1}" as "{operand2}" {logical_operators.get(opr)} "{title2}" as "{operand_2}", then the output contains the following populated JSON schema:\n'

            # {{domain === ''}}
            elif (title1 == title2) and not operand_2 and not operand2:
                msg_content = f'If "{title1}" not specified, then the output contains the following populated JSON schema:\n'

            # {{domain === '' && emailAddress === ''}}
            elif not operand2 and not operand_2 and title1 != title2:
                msg_content = f'If "{title1}" {logical_operators.get(opr)} "{title2}" is not specified, then the output contains the following populated JSON schema:\n'

            # {{domain !== '' && emailAddress === 'some value'}}
            elif not operand2 and operand_2 and title1 != title2:
                msg_content = f'If you choose "{title1}" not specified {logical_operators.get(opr)} "{title2}" as "{operand_2}", then the output contains the following populated JSON schema:\n'

            # {{domain === 'some value' && emailAddress === ''}}
            elif not operand_2 and operand2 and title1 != title2:
                msg_content = f'If you choose "{title2}" not specified {logical_operators.get(opr)} "{title1}" as "{operand2}", then the output contains the following populated JSON schema:\n'

        return msg_content

    except Exception as err:
        print('ERROR: Failed to parse conditional output schema: {0}'.format(err))

def add_supported_action_and_output_schema(md_file_fp, operations):
    md_file_fp.write("\n## Actions supported by the connector\n")
    md_file_fp.write(
        "The following automated operations can be included in playbooks and you can also use the annotations "
        "to access operations from FortiSOAR&trade; release 4.10.0 and onwards:\n")

    md_file_fp.write("<table border=1>")
    md_file_fp.write("<thead>")
    md_file_fp.write("<tr>")
    md_file_fp.write("<th>Function</th>")
    md_file_fp.write("<th>Description</th>")
    md_file_fp.write("<th>Annotation and Category</th>")
    md_file_fp.write("</tr>")
    md_file_fp.write("</thead>")
    md_file_fp.write("<tbody>")

    for action in operations:
        if not (action.get('visible', True) is False or action.get('enabled', True) is False):
            string = "{0} <br/>{1}".format(action.get('annotation', ''), action.get('category', '').capitalize())
            md_file_fp.write("<tr><td>{0}</td>"
                         "<td>{1}</td>"
                         "<td>{2}</td></tr>\n".format(action['title'], action['description'], string))

    md_file_fp.write("</tbody>")
    md_file_fp.write("</table>")
    md_file_fp.write("\n")

    for action in operations:
        if not (action.get('visible', True) is False or action.get('enabled', True) is False):
            md_file_fp.write("\n### operation: {0}\n".format(action['title']))
            md_file_fp.write("#### Input parameters\n")
            if not action['parameters'] or action['parameters'] == [{}]:
                md_file_fp.write("None.\n")
            else:
                md_file_fp.write("<table border=1>")
                md_file_fp.write("<thead>")
                md_file_fp.write("<tr>")
                md_file_fp.write("<th>Parameter</th>")
                md_file_fp.write("<th>Description</th>")
                md_file_fp.write("</tr>")
                md_file_fp.write("</thead>")
                md_file_fp.write("<tbody>")

                for parameter in action['parameters']:
                    string = ""
                    if 'description' in parameter:
                        string = parameter['description']
                    elif 'tooltip' in parameter:
                        string = parameter['tooltip']

                    if 'apiOperation' in parameter:
                        string += ' (This parameter will make an API call named "{0}" to dynamically ' \
                              'populate its dropdown selections)'.format(parameter['apiOperation'])
                    md_file_fp.write("<tr><td>{0}</td>"
                                 "<td>{1}\n".format(parameter['title'], string))
                    if 'onchange' in parameter:
                        md_file_fp.write("<br>")
                        write_onchange_param(md_file_fp, parameter)
                    md_file_fp.write("</td></tr>")
                md_file_fp.write("</tbody>")
                md_file_fp.write("</table>")
                md_file_fp.write("\n")

        # Output Schema for actions----------------------------------------------------------------------------------
            md_file_fp.write("\n#### Output\n")
            if 'output_schema' in action and action['output_schema'] != {} and action['output_schema'] != []:
                md_file_fp.write("The output contains the following populated JSON schema:")
                md_file_fp.write("\n")
                output_schema = action['output_schema']
                write_output_schema(output_schema)
            elif 'conditional_output_schema' in action:
                conditional_output_schema = action['conditional_output_schema']
                md_file_fp.write("The output contains the following populated JSON schema:")
                md_file_fp.write("\n")
                for schema in conditional_output_schema:
                    original_condition = schema.get('condition', '')
                    _condition = original_condition.replace('{', '').replace('}', '')
                    action_parameters = action.get('parameters', [])

                    if '&&' in original_condition:
                        msg_content = extract_multiple_condition(_condition, '&&', action_parameters)
                        md_file_fp.write(msg_content)
                        output_schema = schema.get('output_schema', {})
                        write_output_schema(output_schema)

                    elif '||' in original_condition:
                        msg_content = extract_multiple_condition(_condition, '||', action_parameters)
                        md_file_fp.write(msg_content)
                        output_schema = schema.get('output_schema', {})
                        write_output_schema(output_schema)

                    else:
                        if _condition.startswith("this"):
                            condition = _condition.split()
                        else:
                            condition = _condition.split("'") if "'" in _condition else _condition.split()

                        if isinstance(condition,list ) and len(condition) >= 2:

                            operand1, operator, operand2 = parse_condition(_condition)
                            title = find_param_title(action_parameters, operand1)

                            msg_content = create_message_content(operand2,title, operator)

                        elif isinstance(condition, list) and condition[0] == 'true':
                            msg_content='This is the default output schema:'

                        if msg_content:
                            md_file_fp.write(msg_content)
                            md_file_fp.write("\n")
                            output_schema = schema.get('output_schema', {})
                            write_output_schema(output_schema)
                            md_file_fp.write("\n")
                        msg_content=''
            elif 'output_schema' in action and not (
                    action.get('visible', True) is False or action.get('enabled', True) is False) and action[
                'output_schema'] == {}:
                md_file_fp.write("\n The output contains a non-dictionary value.\n")
            else:
                md_file_fp.write("\n No output schema is available at this time.\n")


def add_sample_playbook_content(info_file_path, md_file_fp, connector_name, version, display_name, operations):
    md_file_fp.write("## Included playbooks\n")
    md_file_fp.write(
        "The `Sample - {0} - {1}` playbook collection comes bundled with the {2} connector. These playbooks contain "
        "steps using which you can perform all supported actions. You can see bundled playbooks in the "
        "**Automation** > **Playbooks** section in FortiSOAR&trade; after importing the {3} "
        "connector.\n".format(connector_name, version, display_name, display_name))
    md_file_fp.write("\n")
    pb_file_fp = get_file_full_path(info_file_path,'playbooks/playbooks.json')
    if pb_file_fp:
        with open(pb_file_fp, 'r') as f:
            json_data = json.load(f)
            workflows = json_data.get('data')[0].get("workflows")
            pb_workflows = sorted(workflows, key=itemgetter('name'))
            for workflow in pb_workflows:
                md_file_fp.write("- {}\n".format(workflow.get("name")))

    else:
        for actions in operations:
            if not (actions.get('visible', True) is False or actions.get('enabled', True) is False):
                md_file_fp.write("- {}\n".format(actions['title']))
    md_file_fp.write(
        "\n**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone "
        "those playbooks and move them to a different collection since the sample playbook collection gets deleted "
        "during connector upgrade and delete.\n")

def add_data_ingestion_section(md_file_fp,display_name):
    md_file_fp.write("## Data Ingestion Support\n")
    md_file_fp.write("Use the Data Ingestion Wizard to easily ingest data into FortiSOAR&trade; by pulling events/alerts/incidents, based on the requirement.\n")
    md_file_fp.write("\n**TODO:** provide the list of steps to configure the ingestion with the screen shots and limitations if any in this section.")



if __name__ == '__main__':
    info_file_path = sys.argv[1]
    if os.path.exists(info_file_path) and info_file_path.endswith('.json'):
        info_json = json.load(open(info_file_path))
        connector_name = info_json.get('name')
        display_name = info_json.get('label')
        version = info_json.get('version')
        vendor_version = info_json.get('vendor_version', '')
        description = info_json.get('description')
        config = info_json.get('configuration')
        operations = info_json.get('operations')
        publisher = info_json.get('publisher', '')
        ingestion_supported = info_json.get('ingestion_supported')
        approved = info_json.get('cs_approved')

        md_file_name = 'cyops-connector-{name}-v{version}.md'.format(name=connector_name, version=version)
        html_file_name = 'cyops-connector-{name}-v{version}.html'.format(name=connector_name, version=version)

        md_file_fp = open(md_file_name, 'w')

        # About the connector ----------------------------------------------------------------------------------------------
        add_about_connector_content(md_file_fp, display_name)

        # - Version information --------------------------------------------------------------------------------------------
        add_version_info(md_file_fp, display_name, version, publisher, approved)

        # Adding Release Notes ---------------------------------------------------------------------------------------------
        adding_release_notes(info_file_path, md_file_fp, display_name, version)

        # Installing the connector -----------------------------------------------------------------------------------------
        add_installing_connector_content(md_file_fp, connector_name)

        # Prerequisites to configuring the connector -----------------------------------------------------------------------
        add_prerequisites_content(md_file_fp, display_name)

        # Minimum Permissions Required -------------------------------------------------------------------------------------
        add_minimum_permission_section(md_file_fp)

        # - Configuration parameters ---------------------------------------------------------------------------------------
        add_configuration_parameters(md_file_fp, display_name, config)

        # Actions supported by the connector -------------------------------------------------------------------------------
        add_supported_action_and_output_schema(md_file_fp, operations)

        # Included playbooks -----------------------------------------------------------------------------------------------
        add_sample_playbook_content(info_file_path, md_file_fp, connector_name, version, display_name, operations)

        # Data Ingestion Support -----------------------------------------------------------------------------------------------
        if ingestion_supported:
            add_data_ingestion_section(md_file_fp, display_name)
        md_file_fp.close()

        html = markdown2.markdown_path(md_file_fp.name, extras=["code-friendly"])
        html_file = open(html_file_name, 'w')
        html_file.write(html)
        html_file.close()

        # os.remove(md_file_name)  # comment out this line to generate .md file
    else:
        print("Info.json file does not exist.")