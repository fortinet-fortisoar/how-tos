#### What's Improved

- Added the following changes:
    - New option for existing playbook.json file: This option will help to avoid regenerating UUID's for existing
      connector actions.
      </br>**"-w", "--workflow_collection": Path to the previous version of the sample workflow collection. eg, /tmp/playbooks.json.**
    - Updated trigger step type of sample playbooks, Alert to Reference.
    - Default value can be pickup from info.json file.
    - Removed step variable from connector action step.