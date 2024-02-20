README_FILE_NAME = 'README.md'
CONTENTS_FILE_NAME = 'contents.md'
SETUP_FILE_NAME = 'setup.md'
USAGE_FILE_NAME = 'usage.md'
DOC_FOLDER_NAME = 'docs'
RESOURCE_FOLDER_NAME = 'res'
CERTIFIED = "NO"

SIGMA_PICKLIST_VALUE = "/api/3/picklists/fa026fd2-2b2f-45b0-80aa-61eda4f9a007"
FORTINET_FABRIC_PICKLIST_VALUE = "/api/3/picklists/8188b8c7-6f77-4f28-8b87-11c7ceef84dc"
YARA_PICKLIST_VALUE = "/api/3/picklists/d2bc7e39-adae-4325-a506-e9e7c06f3420"

SCOPE_LIST = """Fetch CVEs for KEVs: Using NVD integration FortiSOAR checks if an associated CVE is tagged as a KEVs. Once found, it creates the CVE records in the vulnerability module and links those records to outbreak alerts.
Ingest IOCs as Threat Feeds: IOCs associated with the Outbreak are ingested as threat feeds in FortiSOAR using Fortinet FortiGuard Outbreak connector.
Users are notified and the alert severity is raised if an alert containing these IOCs is found in FortiSOAR.
IOC Threat Hunt: You can perform IOC Threat Hunt, and create IOC hunt alerts of typeOutbreakin FortiSOAR, using any of the following:
- Fortinet Fabric solutions (FortiAnalyzer)
- Fortinet Fabric solutions (FortiSIEM)
Remediation: We can take remediation using two ways
- Automatically: FortiSOAR automatically blocks indicators, of type IP and URL, using the FortiGate Integration. For rest of the indicators, a FortiSOAR task is created.
- Manually: FortiSOAR automatically creates a FortiSOAR task to block all the indicators using the FortiGate Integration."""

FUTURE_SCOPE = """IOC Threat Hunt: You can perform IOC Threat Hunt, and create IOC hunt alerts of typeOutbreakin FortiSOAR, using any of the following:
- Other SIEM solutions (QRadar/Splunk) 
Sigma Rules: You can perform signature Based Threat Hunt using Sigma Rules:
- Perform Signature-based Threat Hunting using Fortinet Fabric solutions (FortiSIEM/FortiAnalyzer) and create alerts of typeOutbreakin FortiSOAR
- Perform Signature-based Threat Hunting using other SIEM solutions (QRadar/Splunk/Azure Log Analytics) and create alerts of typeOutbreakin FortiSOAR.
Mitigation: For every Outbreak Alert have associated mitigation. FortiSOAR provides the mitigation recommendations using public sources, like patch available, etc. 
This solution pack depends on the following solution packs:"""

SP_CONTENTS_DATA = [
        ("SOAR Framework", "Solution Pack", "v2.2.0 or later", "Required for Incident Response modules"),
        ("Threat Intel Management", "Solution Pack", "v1.1.0 or later", "Required to ingest threat feeds"),
        ("Vulnerability Management", "Solution Pack", "v1.2.1 or later", "Required to ingest CVEs for KEVs"),
        ("Outbreak Response Framework", "Solution Pack", "v1.0.0 or later", "Helps in investigating Outbreak Alerts")
    ]
