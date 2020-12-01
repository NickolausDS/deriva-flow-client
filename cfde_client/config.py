import globus_automate_client


CONFIG = {
    # Files with dynamic config information in JSON
    "DYNAMIC_CONFIG_LINKS": {
        "prod": ("https://g-5cf005.aa98d.08cc.data.globus.org/submission_dynamic_config/"
                 "cfde_client_config.json?download=0"),
        "staging": ("https://g-5cf005.aa98d.08cc.data.globus.org/submission_dynamic_config/"
                    "cfde_client_config.json?download=0"),
        "dev": ("https://g-5cf005.aa98d.08cc.data.globus.org/submission_dynamic_config/"
                "cfde_client_config.json?download=0")
    },
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
    # Format for BDBag archives
    "ARCHIVE_FORMAT": "zip"
}
# Add all necessary scopes together for Auth call
CONFIG["ALL_SCOPES"] = CONFIG["AUTOMATE_SCOPES"] + [CONFIG["HTTPS_SCOPE"]]
