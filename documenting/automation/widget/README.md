# Widget Documentation

Let's automate widget documentation. Creates FortiSOAR standard required .md files automatically from info.json.

**Input**:
```
Provide widget "tgz" or folder (only).
```

Following is the structure of any widget after document creation: 
```
widget-name
├───README.md
└───docs
      ├───setup.md
      ├───usage.md
      └───res
├───widget
    ├───release_notes.md (If new version)
    ├───info.json
    ├───edit.html
    ├───edit.js
    ├───view.html
    ├───view.js
```

Steps to be followed while creating documentation:
1. Download the doc automation [`Widget-Doc-Automation`](https://github.com/fortinet-fortisoar/how-tos/raw/main/documenting/widget/Widget-Doc-Automation)
2. Unzip the doc automation folder.
3. Execute the `main.py` file with passing **Widget** folder path as parser `--widget-path`.
   
Example:
```
/usr/bin/python3 /Users/xyz/downloads/Widget-Doc-Automation/main.py --widget-path /Users/xyz/Documents/widget-name.tgz
```

> **Note**
1. Specify solution pack usage under `usage.md` file.
