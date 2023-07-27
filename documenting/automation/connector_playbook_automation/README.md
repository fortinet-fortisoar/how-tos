# connector-playbook-automation

Playbook Automation:

-Input Parameters:

	optional arguments:
      -h, --help            show this help message and exit
      -c CONNECTOR_INFO, --connector_info CONNECTOR_INFO Provide connectors info.json file path
      -o OUTPUT, --output OUTPUT Provide output directory path
      -w WORKFLOW_COLLECTION, --workflow_collection WORKFLOW_COLLECTION
                        Path to the previous version of the sample workflow collection. eg, /tmp/playbooks.json

-Result:

	Creates sample playbook collection JSON file.

-Usage:

    python generate_sample_playbook [-h] -c CONNECTOR_INFO [-o OUTPUT] [-j PLAYBOOK_JSON]

Details:
-
- This script(generate_sample_playbook.py) generates new sample playbook collection, required to ship with connector.
- Python package dependency configparser==3.5.0.
- Script generates a sample playbook collection, consists of playbook for each connector action. Resulted filename will
  be "Sample - [CONNECTOR NAME] - [CONNECTOR.VERSION].json".
- User can import the sample playbook collection into FortiSOAR.
- Refer following example.
    1. python generate_sample_playbook.py --connector_info info.json --output /home/user/playbooks/
    2. python generate_sample_playbook.py --connector_info info.json --workflow_collection /tmp/playbook.json --output /home/user/playbooks/
