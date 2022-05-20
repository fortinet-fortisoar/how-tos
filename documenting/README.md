# Connector-documentation

Let's automate connector documentation.
Creates .md, and .html (optional) files automatically from info.json.

Dependencies:

`pip3 install markdown2`

Usage: 

```
python3 autodocs.py /path/to/info.json --html
python3 autodocs.py /path/to/info.json --md
python3 autodocs.py /path/to/info.json --html --md
```

Output file(s) will be created in the same directory where the script file is. 

Output file type depend on the file arguments provided.

# Solution Pack-documentation

Please download 'SP-Doc-Template.zip', extract and add them in respective solution pack repo.
Following is a structure of a solution pack repo for docs;

solution-pack-name\
│---README.md\
│\
└───docs\
      │---contents.md\
      │---setup.md\
      │---usage.md\
      └───res\
           │---screenshot1.png\
           │---screenshot2.png\
           └───screenshot3.png\
 
The attachment is a zipped file following this template and the illustrated folder structure with a brief description of each heading and topics.
