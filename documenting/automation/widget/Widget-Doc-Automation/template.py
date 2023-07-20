from string import Template

# README
readme = Template(
    '# Release Information\n- **Version**: $version\n- **Certified**: $certify\n- **Publisher**: $publisher\n- **Compatibility**: $compatible_version\n- **Applicable**: $applicable\n$release_note\n\n# Overview\n$overview\n\n# Next Steps\n| [Installation](./$docs_name/$setup_file#installation) | [Configuration](./$docs_name/$setup_file#configuration) | [Usage](./$docs_name/$usage_file) |\n| ---------------------------------------------- | ------------------------------------------------ | -------------------------- |')
setup = Template('| [Home](../$readme_file) |\n|--------------------------------------------|\n\n# Installation\n1. To install a widget, click **Content Hub** > **Discover**.\n2. From the list of widget that appears, search for and select **$widget_title**.\n3. Click the **$widget_title** widget card.\n4. Click **Install** on the bottom to begin installation.\n\n# Configuration\n**$widget_title Settings**\n\n[//]: <> (Please add necessary settings for widget.)\n\n| [Usage](./$usage_file) |\n|---------------------|')
usage = Template(
    '| [Home](../$readme_file) |\n|----------------------|\n\n# Usage\n\n[//]: <> (Please add usage of widget.)\n\n| [Installation](./$setup_file#installation) | [Configuration](./$setup_file#configuration) |\n|-----------------------------------------|-------------------------------------------|')
release_note = Template(
    '# What\'s New\n\n[//]: <> (Please add release note of widget.)')
