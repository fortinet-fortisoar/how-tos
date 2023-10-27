from string import Template

# readme
version_data = Template('- **Version**: $version')
certified_data = Template('- **Certified**: $certify')
compatible_version_data = Template('- **Compatible Version**: FortiSOAR $compatible_version')
readme = Template('# Release Information \n\n$version_data \n$certified_data \n- **Publisher**: $publisher \n$compatible_version_data \n$release_note \n\n # Overview \n $overview \n\n # Next Steps\n | [Installation](./$docs_name/setup.md#installation) | [Configuration](./$docs_name/setup.md#configuration) | [Usage](./$docs_name/usage.md) | [Contents](./$docs_name/contents.md) | \n |--------------------------------------------|----------------------------------------------|------------------------|------------------------------|')


# dashboard, modules, global variables, roles, report, widget, rule
name_description_data = Template('| $name | $description |')

# picklist, navigations
name_data = Template('| $name |')

# dashboard
# dashboards_sub_data = Template('| $name | $description |')
dashboards_data = Template('## Dashboards\n\n|Name|Description|\n| :- | :- |\n$dashboards_sub_data')

# picklist
# picklists_sub_data = Template('| $name |')
picklists_data = Template('## Picklist\n\n|Name|\n| :- |\n$picklists_sub_data')

# modules
# modules_sub_data = Template('| $name | $description |')
modules_data = Template('## Module Schema\n\n|Name|Description|\n| :- | :- |\n$modules_sub_data')

# global variables
# global_variables_sub_data = Template('| $name | $description |')
global_variables_data = Template('## Global Variable\n\n|Name|Description|\n| :- | :- |\n$global_variables_sub_data')

# roles
# roles_sub_data = Template('| $name | $description |')
roles_data = Template('## Roles\n\n|Name|Description|\n| :- | :- |\n$roles_sub_data')

# report
# report_sub_data = Template('| $name | $description |')
report_head = Template('## Report\n\n| Name | Description |\n| :- | :- |\n$report_sub_data')

# record set
record_sets_sub_data = Template('| $data1 | $data2 |')
record_sets_data = Template('## $record_name Record set \n\n| Name | Description |\n| :- | :- |\n$record_sets_sub_data')

# connectors
connectors_sub_data = Template('| $name | $description |')
connectors_data = Template('## Connector\n\n| Name | Description |\n| :- | :- |\n$connectors_sub_data')

# widget
# widgets_sub_data = Template('| $name | $description |')
widgets_data = Template('## Widgets\n\n| Name | Description |\n| :- | :- |\n$widgets_sub_data')

# playbooks
playbooks_sub_sub_data = Template('| $name | $description |')
playbooks_sub_data = Template('| $name |\n|:------------:|\n\n| Playbook Name | Description |\n| :- | :- |\n$playbooks_sub_sub_data\n')
playbooks_data = Template('## Playbook Collection\n\n$playbooks_sub_data')

# playbook blocks
playbook_blocks_sub_data = Template('| $name | $description |')
playbook_blocks_data = Template('## Reference Blocks\n\n| Name | Description |\n| :- | :- |\n$playbook_blocks_sub_data')

# rules
# rules_sub_data = Template('| $name | $description |')
rules_data = Template('## Rules\n\n| Name | Description |\n| :- | :- |\n$rules_sub_data')

# navigations
# navigations_sub_data = Template('| $name |')
navigations_data = Template('## System View\n\n| Name |\n| :- |\n$navigations_sub_data')

# contents
content = Template('| [Home](../$readme_file) |\n | -------------------------------------------- |\n\n  # Contents\n\nThe **$solution_name** solution pack contains the following resources.\n\n$dashboards_data\n$picklists_data\n$modules_data\n$connectors_data\n$widgets_data\n$global_variables_data\n$roles_data\n$report_head\n$record_sets_data\n$rules_data\n$playbooks_data\n$playbook_blocks_data\n$navigations_data\n\n>**Warning:** We recommend that you clone these playbooks before customizing to avoid loss of information while upgrading the solution pack.\n\n# Next Steps\n| [Installation](./setup.md#installation) | [Configuration](./setup.md#configuration) | [Usage](./usage.md) |\n| ----------------------------------------- | ------------------------------------------- | --------------------- |')

# prerequisites
prerequisites_sub_data = Template('| $spname | $version | $purpose |')
prerequisites_data = Template('## Prerequisites\nThe **$solution_name** solution pack depends on the following solution packs that are installed automatically &ndash; if not already installed.\n| Solution Pack Name | Version | Purpose |\n| :--------------------- | :---------------------| :--------------------------------------- |\n$prerequisites_sub_data\n\n')

# setup
setup_connectors_data = Template('>* **$connector_name** - $connector_description. To configure and use the $connector_name connector, refer to [Configuring $connector_name]($connector_doc_link)')
setup = Template('[Home](../$readme_file) |\n|--------------------------------------------|\n\n# Installation\n\n1. To install a solution pack, click **Content Hub** > **Discover**.\n2. From the list of solution pack that appears, search for and select **$solution_name**.\n3. Click the **$solution_name** solution pack card.\n4. Click **Install** on the lower part of the screen to begin the installation.\n\n$prerequisites_data\n# Configuration\nFor optimal performance of **$solution_name** solution pack, you can install and configure the connectors that help with the following:\n\n$setup_connectors_data\n\n# Next Steps\n| [Usage](./usage.md) | [Contents](./contents.md) |\n|---------------------|---------------------------|')

# usage
usage = Template('[Home](../$readme_file) |\n | -------------------------------------------- |\n\n# Usage\n\nRefer to [Simulate Scenario documentation](https://github.com/fortinet-fortisoar/solution-pack-soc-simulator/blob/develop/docs/usage.md) to understand how to simulate and reset scenarios.\n\nTo understand the process FortiSOAR follows to respond to <SP Specific threat>. We have included the following scenario with this solution pack:\n- Scenario 1\n- Scenario 2\n\nRefer to the subsequent sections to understand how this solution pack\'s automation addresses your needs.\n\n## Scenario 1\n\n## Scenario 2\n\n# Next Steps\n| [Installation](./setup.md#installation) | [Configuration](./setup.md#configuration) | [Contents](./contents.md) |\n| ----------------------------------------- | ------------------------------------------- | --------------------------- |')

# release note
release_note = Template('# What\'s New\n\n## Enhancements\n\n## Resolved Issues')
