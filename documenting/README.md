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

Please download and extract 'SP-Doc-Template.zip'. Add extracted folder in respective solution pack repo.
Following is the structure of any solution pack repo after you paste document template in it;

```
solution-pack-name
│---README.md
│
└───docs
      │---contents.md
      |---setup.md
      │---usage.md
      └───res
          │---screenshot1.png
          │---screenshot2.png
          └───screenshot3.png
 ```
 
The attachment is a zipped file following this template and the illustrated folder structure with a brief description of each heading and topics.

| File Name | Description |
|:----------|:------------|
|`readme.md`| Landing page for any Solution Pack. Please add this file in repo root folder |
|`docs/` folder | Contains all supporting docs and images folder. Place this folder in repo root folder |
| `docs/res` folder | Contains supporting images. Place this folder inside the `docs/` folder |
|`docs/content.md`| Contains the list of contents of this solution packs. Place this file inside the `docs/` folder|
|`docs/setup.md`| Contains installation and configuration instructiions for this solution pack. Place this file inside the `docs/` folder|
|`docs/usage.md`| Contains instructions on use cases/simulations/demo contained in the solution pack. Place this file inside the `docs/` folder|

