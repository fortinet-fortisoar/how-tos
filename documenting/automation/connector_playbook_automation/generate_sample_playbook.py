#!/usr/bin/env python
import json, sys, argparse, uuid, configparser

config = {}

# Need to get this values from database
# Database Name: venom
# Table Name: workflow_step_types
# Field Name: uuid
alert_workflow_step_types_uuid = "b348f017-9a94-471f-87f8-ce88b6a7ad62"
connector_step_workflow_step_types_uuid = "0bfed618-0316-11e7-93ae-92361f002671"


def read_json_file(connector_info):
    try:
        with open(connector_info, 'r') as data:
            json_data = json.load(data)
        return json_data
    except Exception as err:
        print("read_json_file: " + str(err))
        raise Exception("read_json_file: " + str(err))


def create_alert_step(playbook_template_steps=None):
    try:
        if playbook_template_steps:
            step_template = playbook_template_steps
            arguments_data = playbook_template_steps.get("arguments", {})
        else:
            step_template = {}
            step_template["uuid"] = str(uuid.uuid4())
            arguments_data = {}

        step_template["@type"] = "WorkflowStep"
        step_template["name"] = config.get('Alert_Step_Info', 'Alert_Step_Name')
        step_template["description"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Description'))
        step_template["status"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Status'))
        arguments_data["step_variables"] = eval(config.get('Alert_Step_Info', 'Alert_Step_Arguments_step_variables'))

        arguments_data.pop("route", None)
        arguments_data.pop("title", None)
        arguments_data.pop("resources", None)
        arguments_data.pop("inputVariables", None)
        arguments_data.pop("executeButtonText", None)
        arguments_data.pop("noRecordExecution", None)
        arguments_data.pop("singleRecordExecution", None)
        step_template["arguments"] = arguments_data
        step_template["left"] = config.get('Alert_Step_Info', 'Alert_Step_Left')
        step_template["top"] = config.get('Alert_Step_Info', 'Alert_Step_top')
        step_template["stepType"] = "/api/3/workflow_step_types/" + alert_workflow_step_types_uuid
        return step_template
    except Exception as err:
        print("create_alert_step: " + str(err))


def get_parameters(parameters):
    try:
        params = {}
        for p in parameters:
            if p.get("value"):
                params[p["name"]] = p["value"]
            else:
                params[p["name"]] = ""
        return params if params != {} else []
    except Exception as err:
        print("get_parameters: " + str(err))


def create_connector_action_step(connector_name, connector_label, function_title, connector_version, function_operation,
                                 parameters, playbook_template_steps=None):
    try:
        if playbook_template_steps:
            step_template = playbook_template_steps
            arguments_data = playbook_template_steps.get("arguments", {})
        else:
            step_template = {}
            step_template["uuid"] = str(uuid.uuid4())
            arguments_data = {}
            arguments_data["name"] = connector_label

        step_template["@type"] = "WorkflowStep"
        step_template["name"] = function_title
        step_template["description"] = eval(config.get('Connector_Step_Info', 'Connector_Step_Description'))
        step_template["status"] = eval(config.get('Connector_Step_Info', 'Connector_Step_Status'))

        arguments_data["config"] = config.get('Connector_Step_Info', 'Connector_Step_Arguments_config')
        arguments_data["params"] = get_parameters(parameters)
        arguments_data["version"] = connector_version
        arguments_data["connector"] = connector_name
        arguments_data["operation"] = function_operation
        arguments_data["operationTitle"] = function_title
        step_template["arguments"] = arguments_data
        step_template["left"] = config.get('Connector_Step_Info', 'Connector_Step_Left')
        step_template["top"] = config.get('Connector_Step_Info', 'Connector_Step_top')
        step_template["stepType"] = "/api/3/workflow_step_types/" + connector_step_workflow_step_types_uuid
        return step_template
    except Exception as err:
        print("create_connector_action_step: " + str(err))


def create_routes(function_title, alert_step_uuid, connector_function_step_uuid, playbook_template_route_steps=None):
    try:
        if playbook_template_route_steps:
            routes_template = playbook_template_route_steps
        else:
            routes_template = {}
            routes_template["uuid"] = str(uuid.uuid4())

        routes_template["@type"] = "WorkflowRoute"
        routes_template["label"] = eval(config.get('Routes_Info', 'Routes_Label'))
        routes_template["isExecuted"] = config.getboolean('Routes_Info', 'Routes_isExecuted')
        routes_template["name"] = config.get('Alert_Step_Info', 'Alert_Step_Name') + "-> " + function_title
        routes_template["sourceStep"] = "/api/3/workflow_steps/" + alert_step_uuid
        routes_template["targetStep"] = "/api/3/workflow_steps/" + connector_function_step_uuid
        return routes_template
    except Exception as err:
        print("create_routes: " + str(err))


def get_workflow_details(function, collection_data):
    for wf in collection_data:
        if wf["name"].lower() == function["title"].lower():
            return wf
    return {}


def create_workflow(collection_UUID, info_file_json, collection_data=None):
    try:
        all_functions = info_file_json["operations"]
        if collection_data:
            all_playbooks_list = collection_data
        else:
            all_playbooks_list = []
        for function in all_functions:
            try:
                # Skip to add playbook if action visible is false or if enabled is false.
                if function.get("visible", True) == False or function.get("enabled", True) == False:
                    continue
            except Exception as err:
                print("create_workflow: " + str(err))

            # check if action exist or not
            if collection_data:
                playbook_template = get_workflow_details(function, collection_data)
            else:
                playbook_template = {}

            new_workflow = False
            if not playbook_template.get("uuid"):
                playbook_template["@type"] = "Workflow"
                playbook_template["uuid"] = str(uuid.uuid4())
                new_workflow = True

            alert_step_pos = 0
            # This function create alert step.
            if playbook_template.get("steps"):
                if alert_workflow_step_types_uuid in playbook_template["steps"][0]["stepType"] \
                        or "f414d039-bb0d-4e59-9c39-a8f1e880b18a" in playbook_template["steps"][0]["stepType"]:
                    playbook_template_alert_steps = playbook_template["steps"][0]
                    playbook_template_action_steps = playbook_template["steps"][1]
                else:
                    playbook_template_action_steps = playbook_template["steps"][0]
                    playbook_template_alert_steps = playbook_template["steps"][1]
                    alert_step_pos = 1
                alert_step = create_alert_step(playbook_template_steps=playbook_template_alert_steps)
            else:
                alert_step = create_alert_step()

            # This function create connector step.
            if playbook_template.get("steps"):
                connector_function_step = create_connector_action_step(info_file_json["name"], info_file_json["label"],
                                                                       function["title"], info_file_json["version"],
                                                                       function["operation"], function["parameters"],
                                                                       playbook_template_steps=playbook_template_action_steps)
            else:
                connector_function_step = create_connector_action_step(info_file_json["name"], info_file_json["label"],
                                                                       function["title"], info_file_json["version"],
                                                                       function["operation"], function["parameters"])
            if collection_UUID:
                playbook_template["collection"] = "/api/3/workflow_collections/" + collection_UUID
            if alert_step_pos == 0:
                playbook_template["steps"] = [alert_step, connector_function_step]
            else:
                playbook_template["steps"] = [connector_function_step, alert_step]
            playbook_template["triggerLimit"] = eval(config.get('Workflow_Info', 'Workflow_TriggerLimit'))  # None
            playbook_template["description"] = function["description"]
            playbook_template["name"] = function["title"]
            playbook_template["tag"] = "#" + info_file_json["label"]
            playbook_template["recordTags"] = get_tags(info_file_json)
            playbook_template["isActive"] = config.getboolean('Workflow_Info', 'Workflow_isActive')  # False
            playbook_template["debug"] = config.getboolean('Workflow_Info', 'Workflow_Debug')  # False
            playbook_template["singleRecordExecution"] = config.getboolean('Workflow_Info',
                                                                           'Workflow_singleRecordExecution')  # False
            playbook_template["parameters"] = []
            playbook_template["synchronous"] = config.getboolean('Workflow_Info', 'Workflow_synchronous')  # False
            playbook_template["triggerStep"] = "/api/3/workflow_steps/" + alert_step["uuid"]

            if playbook_template.get("routes"):
                playbook_template["routes"] = [
                    create_routes(function["title"], alert_step["uuid"], connector_function_step["uuid"],
                                  playbook_template_route_steps=playbook_template.get("routes")[0])]
            else:
                playbook_template["routes"] = [
                    create_routes(function["title"], alert_step["uuid"], connector_function_step["uuid"])]
            if new_workflow:
                all_playbooks_list.append(playbook_template)
        return all_playbooks_list
    except Exception as err:
        print("create_workflow: " + str(err))


def get_tags(info_file_json):
    recordTags = eval(config.get('Alert_Step_Info', 'Alert_Step_Tags'))
    if not recordTags:
        name = info_file_json.get("name", "")
        if name:
            recordTags = [name.split("-")[0].capitalize(), name]
        else:
            raise Exception("connector name not found.")
    return recordTags


def create_collection(info_file_json, existing_playbook_json):
    try:
        new_playbook_collection = {}
        collection_data = {}
        if existing_playbook_json:
            collection_data = existing_playbook_json.get("data")[0]
            collection_data["workflows"] = create_workflow(collection_data.get("uuid"), info_file_json,
                                                           collection_data=collection_data.get("workflows"))
        else:
            collection_data["uuid"] = str(uuid.uuid4())
            collection_data["@type"] = "WorkflowCollection"
            # This function create playbook workflows.
            collection_data["workflows"] = create_workflow(collection_data["uuid"], info_file_json)

        collection_data["name"] = "Sample - {Dummy_Connector} - {connector_version}".format(
            Dummy_Connector=info_file_json["label"], connector_version=info_file_json["version"])
        collection_data["description"] = info_file_json["description"]
        if not collection_data.get("visible"):
            collection_data["visible"] = eval(config.get('Collection_Info', 'Collection_Visible'))
        if not collection_data.get("visible"):
            collection_data["image"] = eval(config.get('Collection_Info', 'Collection_Image'))
        collection_data["recordTags"] = get_tags(info_file_json)
        new_playbook_collection["type"] = "workflow_collections"
        new_playbook_collection["data"] = [collection_data]
        return new_playbook_collection
    except Exception as err:
        print("create_collection: " + str(err))


def set_cmd_arguments():
    try:
        parser = argparse.ArgumentParser(prog='generate_sample_playbook')
        parser.add_argument("-c", "--connector_info", help="Provide connectors info.json file path", required=True)
        parser.add_argument("-o", "--output", help="Provide output directory path", default=".")
        parser.add_argument("-w", "--workflow_collection",
                            help="Path to the previous version of the sample workflow collection. eg, /tmp/playbooks.json",
                            default=None)
        args = parser.parse_args()

        return args
    except Exception as err:
        print("set_cmd_arguments: " + str(err))


def read_config_file():
    try:
        config = configparser.RawConfigParser()
        config.read("config.ini")
        return config
    except Exception as err:
        print("read_config_file: " + str(err))


def main():
    try:
        args = set_cmd_arguments()
        global config
        config = read_config_file()
        # This function read connector info.json file for get function details.
        info_file_json = read_json_file(args.connector_info)

        # check if existing playbook.json file is provided.
        existing_playbook_json = None
        if args.workflow_collection:
            existing_playbook_json = read_json_file(args.workflow_collection)

        # This function create new collection for given connector.
        new_playbook_collection = create_collection(info_file_json, existing_playbook_json)

        # Dump generated collection into JSON file.
        with open("{path}/Sample - {Dummy_Connector} - {Connector_Version}.json".format(
                Dummy_Connector=info_file_json["label"], path=args.output, Connector_Version=info_file_json["version"]),
                'w') as outfile:
            json.dump(new_playbook_collection, outfile, indent=2)
    except Exception as err:
        print(str(err))


if __name__ == "__main__":
    main()
