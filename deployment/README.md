# Client Deployment

This directory contains extra deployment config files critical for running the
Deriva Flow Client.

### Client Config

The ``cfde_client_config.json`` file lists the global configuration each user
will pull from when running the Deriva Flow Client tool. The config exists on a
public Globus endpoint and is used by each client regardless of version.

Current Deployment exists on the GCS CFDE Prod endpoint

https://g-5cf005.aa98d.08cc.data.globus.org/submission_dynamic_config/cfde_client_config.json

#### Client Config Testing

Test the latest config by running a data submission through it: 

```
cfde run --service-instance dev datapackage_0631cefb6a1cfff0ef4ecbf6931421add27f5884.zip
```

Delete the submission afterwards with the following lines: 
