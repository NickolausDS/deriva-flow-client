import globus_automate_client


CONFIG = {
    # File with dynamic config information in JSON
    # Contains:
    #   CATALOGS (dict): keyword: catalog_name
    #   FLOWS (dict): keyword: flow_id
    #   MIN_VERSION (str): The minimum version of the client required
    "DYNAMIC_CONFIG_LINK": "https://317ec.36fe.dn.glob.us/public/CFDE/cfde_client_config.json",
    # Translations for Automate states into nicer language
    "STATE_MSGS": {
        "ACTIVE": "is still in progress",
        "INACTIVE": "has stalled, and may need help to resume",
        "SUCCEEDED": "has completed successfully",
        "FAILED": "has failed"
    },
    # Automate Scopes
    "HTTPS_SCOPE": "https://auth.globus.org/scopes/0e57d793-f1ac-4eeb-a30f-643b082d68ec/https",
    "AUTOMATE_SCOPES": list(globus_automate_client.flows_client.ALL_FLOW_SCOPES),
    # FAIR Research Endpoint destination directory and HTTPS URL
    "EP_DIR": "/public/CFDE/metadata/",
    "EP_UUID": "0e57d793-f1ac-4eeb-a30f-643b082d68ec",
    "EP_URL": "https://317ec.36fe.dn.glob.us",
    # Format for BDBag archives
    "ARCHIVE_FORMAT": "zip"
}
# Add all necessary scopes together for Auth call
CONFIG["ALL_SCOPES"] = CONFIG["AUTOMATE_SCOPES"] + [CONFIG["HTTPS_SCOPE"]]
