# connector-documentation

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
