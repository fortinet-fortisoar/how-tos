# Solution Pack Documentation

Let's automate solution pack documentation. Creates FortiSOAR standard required .md files automatically from info.json.

**Input**:
```
Provide solution pack "zip" or "unzipped" folder (only).
```

Following is the structure of any solution pack after document creation: 
```
solution-pack-name
├───README.md
├───release_notes.md (If new version)
└───docs
      ├───contents.md
      ├───setup.md
      ├───usage.md
      └───res
```

Steps to be followed while creating documentation:
1. Download the doc automation [`SP-Doc-Automation.zip`](https://github.com/fortinet-fortisoar/how-tos/blob/main/documenting/automation/solution-pack/SP-Doc-Automation.zip)
2. Unzip the doc automation folder.
3. Execute the `main.py` file with passing **Solution Pack** folder path as parser `--sp-path`.
   
Example:
```
/usr/bin/python3 /Users/xyz/downloads/SP-Doc-Automation/main.py --sp-path /Users/xyz/Documents/solution-pack-name.zip
```

> **Note**
1. Automation ignore record for `Queue` and `SLA Templates`.
2. Record set get created only for `Scenario` and `Attachment`. Please add other record set if used.
3. Add connector doc link for each used connector under `setup.md` file.
4. Specify solution pack usage under `usage.md` file.