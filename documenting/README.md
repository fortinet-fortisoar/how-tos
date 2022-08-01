# Connector-documentation

Let's automate connector documentation.
Creates .md, and .html (optional) files automatically from info.json.

Dependencies:

```
pip3 install markdown2
```

Usage: 

```bash
python3 autodocs.py /path/to/info.json --html
python3 autodocs.py /path/to/info.json --md
python3 autodocs.py /path/to/info.json --html --md
```

Output file(s) will be created in the same directory where the script file is. 

Output file type depend on the file arguments provided.

# Solution Pack Documentation

1. Download and extract [`SP-Doc-Template.zip`](https://github.com/fortinet-fortisoar/how-tos/raw/main/documenting/SP-Doc-Template.zip).
2. Copy the extracted folder to the solution pack folder.
3. Following is the structure of any solution pack repo after you paste the document template:

```
solution-pack-name
├───README.md
└───docs
      ├───contents.md
      ├───setup.md
      ├───usage.md
      └───res
          ├───screenshot1.png
          ├───screenshot2.png
          └───screenshot3.png
```

The zipped file contains the following files and folders.

| File Name         | Description                                                                                                                   |
|:------------------|:------------------------------------------------------------------------------------------------------------------------------|
| `README.md`       | Landing page for any Solution Pack. Please add this file in repo root folder                                                  |
| `docs/` folder    | Contains all supporting docs and images folder. Place this folder in repo root folder                                         |
| `docs/res` folder | Contains supporting images. Place this folder inside the `docs/` folder                                                       |
| `docs/content.md` | Contains the list of contents of this solution packs. Place this file inside the `docs/` folder                               |
| `docs/setup.md`   | Contains installation and configuration instructions for this solution pack. Place this file inside the `docs/` folder        |
| `docs/usage.md`   | Contains instructions on use cases/simulations/demo contained in the solution pack. Place this file inside the `docs/` folder |

## Updates to an Existing Solution Pack

1. Download and extract [`SP-Update-Doc-Template.zip`](https://github.com/fortinet-fortisoar/how-tos/raw/main/documenting/SP-Update-Doc-Template.zip).
2. Copy the extracted folder to the solution pack folder.
3. Following is the structure of any solution pack repo after you paste the document template:

```
solution-pack-name
├───README.md
├───release_notes.md
└───docs
      ├───contents.md
      ├───setup.md
      ├───usage.md
      └───res
          ├───screenshot1.png
          ├───screenshot2.png
          └───screenshot3.png
```
The zipped file contains the following files and folders.

| File Name          | Description                                                                                                                   |
|:-------------------|:------------------------------------------------------------------------------------------------------------------------------|
| `README.md`        | Landing page for any Solution Pack. Please add this file in repo root folder                                                  |
| `release_notes.md` | Contains updates to an existing solution pack &ndash; in a specific format. Please add this file in repo root folder          |
| `docs/` folder     | Contains all supporting docs and images folder. Place this folder in repo root folder                                         |
| `docs/res` folder  | Contains supporting images. Place this folder inside the `docs/` folder                                                       |
| `docs/content.md`  | Contains the list of contents of this solution packs. Place this file inside the `docs/` folder                               |
| `docs/setup.md`    | Contains installation and configuration instructions for this solution pack. Place this file inside the `docs/` folder        |
| `docs/usage.md`    | Contains instructions on use cases/simulations/demo contained in the solution pack. Place this file inside the `docs/` folder |
