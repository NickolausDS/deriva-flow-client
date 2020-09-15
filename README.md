# CFDE Client

This is a client to interact with the Globus Automate Flows for CFDE use cases. Both a Python API and a CLI tool are available.

# Installation

The CFDE Client requires Python 3.6 or later. To check which version of Python you have, run `python --version`. If you have both Python 2 and Python 3 installed, you may need to check with `python3 --version`. If this is the case, you will also need to use `pip3` instead of `pip` below.

```
git clone https://github.com/fair-research/deriva-flow-client.git
cd deriva-flow-client
pip install -e .
```

# Usage
This tool can ingest any of the following into DERIVA:

1. A directory to be formatted into a BDBag
2. A Git repository to be copied into a BDBag
3. A premade BDBag directory
4. A premade BDBag in an archive file

In all cases, the data must already be in CFDE TableSchema format, or the ingest may fail. See instructions here (link to docs pending).


### Command line
There are four commands available: `run`, `status`, `login`, and `logout`. Use them as follows:

- `cfde run DATA-PATH` will ingest the data found at `DATA-PATH` into DERIVA. You can also specify the following options:
    - `--catalog-id=CATALOG_ID` will ingest into an existing catalog instead of creating a new catalog.
    - `--output-dir=OUTPUT_DIR` will copy the data in `DATA-PATH`, if it is a directory, to the location you specify, which must not exist and must not be inside `DATA-PATH`. The resulting BDBag will be named after the output directory. If not specified, the BDBag will be created in-place in `DATA_PATH` if necessary.
    - `--delete-dir` will trigger deletion of the `output-dir` after processing is complete. If you didn't specify `output-dir`, this option has no effect.
    - `--ignore-git` will prevent the client from overwriting `output-dir` and `delete-dir` to handle Git repositories.

- `cfde status` will check the status of a Flow instance. By default, the last run Flow is used, but if you want to check a previous Flow you can provide one or both of the following options:
    - `--flow-id=ID` is the ID of the Flow itself (NOT a specific instance of the Flow).
    - `--flow-instance-id=ID` is the ID of the particular instance/invocation of the Flow you want to check.

- `cfde login` will start the login process. If you have tokens saved from a previous login, this command will validate those tokens and only re-authenticate you if they are expired. It is not necessary to run this command before `run` or `status`, because those commands will also authenticate you if needed.

- `cfde logout` will log you out and revoke any valid cached tokens.


### Python API
The `CfdeClient` class, once instantiated, has the following methods:

- `start_deriva_flow(self, data_path, catalog_id=None, output_dir=None, delete_dir=False, **kwargs)`
- `check_status(self, flow_id=None, flow_instance_id=None, raw=False)`
- `logout(self)`

The arguments operate in the same fashion as the CLI options, and are documented in detail in the method docstrings.
