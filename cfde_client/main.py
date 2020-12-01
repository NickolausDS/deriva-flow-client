from io import StringIO
import json
import os
import sys

import click

from cfde_client import CfdeClient


DEFAULT_STATE_FILE = os.path.expanduser("~/.cfde_client.json")


@click.group()
def cli():
    """Client to interact with the DERIVA Action Provider and associated Flows."""
    pass


@cli.command()
@click.argument("data-path", nargs=1, type=click.Path(exists=True))
@click.option("--dcc-id", "--dcc", default=None, show_default=True)
@click.option("--catalog", default=None, show_default=True)
@click.option("--schema", default=None, show_default=True)
@click.option("--acl-file", default=None, show_default=True, type=click.Path(exists=True))
@click.option("--output-dir", default=None, show_default=True, type=click.Path(exists=False))
@click.option("--delete-dir/--keep-dir", is_flag=True, default=False, show_default=True)
@click.option("--ignore-git/--handle-git", is_flag=True, default=False, show_default=True)
@click.option("--dry-run", is_flag=True, default=False, show_default=True)
@click.option("--test-submission", "--test-sub", "--test-drive", is_flag=True,
              default=False, show_default=True)
@click.option("--verbose", "-v", is_flag=True, default=False, show_default=True)
@click.option("--force-login", is_flag=True, default=False, show_default=True)
# TODO: Debug "hidden" missing parameter
@click.option("--no_browser", is_flag=True, default=False)  # , hidden=True)
@click.option("--server", default=None)  # , hidden=True)
@click.option("--force-http", is_flag=True, default=False)  # , hidden=True)
@click.option("--bag-kwargs-file", type=click.Path(exists=True), default=None)  # , hidden=True)
@click.option("--client-state-file", type=click.Path(exists=True), default=None)  # , hidden=True)
@click.option("--service-instance", default=None)  # , hidden=True)
def run(data_path, dcc_id, catalog, schema, acl_file, output_dir, delete_dir, ignore_git,
        dry_run, test_submission, verbose, force_login, no_browser, server, force_http,
        bag_kwargs_file, client_state_file, service_instance):
    """Start the Globus Automate Flow to ingest CFDE data into DERIVA."""
    # Get any saved parameters
    if not client_state_file:
        client_state_file = DEFAULT_STATE_FILE
    try:
        with open(client_state_file) as f:
            state = json.load(f)
        if verbose:
            print("Loaded previous state")
    except FileNotFoundError:
        state = {}
        if verbose:
            print("No previous state found")

    # Read bag_kwargs_file if provided
    if bag_kwargs_file:
        with open(bag_kwargs_file) as f:
            bag_kwargs = json.load(f)
    else:
        bag_kwargs = {}
    # Read acl_file if provided
    if acl_file:
        with open(acl_file) as f:
            dataset_acls = json.load(f)
    else:
        dataset_acls = None

    # Determine DCC ID to use
    if verbose:
        print("Determining DCC")
    # If user supplies DCC as option, will always use that
    # If supplied DCC is different from previously saved DCC, prompt to save,
    #   unless user has not saved DCC or disabled the save prompt
    state_dcc = state.get("dcc_id")
    never_save = state.get("never_save")
    if not never_save and dcc_id is not None and state_dcc is not None and state_dcc != dcc_id:
        if verbose:
            print("Saved DCC '{}' mismatch with provided DCC '{}'".format(state_dcc, dcc_id))
        save_dcc = (input("Would you like to save '{}' as your default DCC ID ("
                          "instead of '{}')? y/n: ".format(dcc_id, state_dcc))
                    .strip().lower() in ["y", "yes"])
        if not save_dcc:
            if (input("Would you like to disable this prompt permanently? y/n:").strip().lower()
                    in ["y", "yes"]):
                state["never_save_dcc"] = True
    elif dcc_id is None and state_dcc is not None:
        dcc_id = state_dcc
        save_dcc = False
        print("Using saved DCC '{}'".format(dcc_id))
    elif dcc_id is None and state_dcc is None:
        if verbose:
            print("No saved DCC ID found and no DCC provided")
        dcc_id = input("Please enter the CFDE identifier for your "
                       "Data Coordinating Center: ").strip()
        save_dcc = input("Thank you. Would you like to save '{}' for future submissions? "
                         "y/n: ".format(dcc_id)).strip().lower() in ["y", "yes"]
    # Save DCC ID in state if requested
    if save_dcc:
        state["dcc_id"] = dcc_id
        if verbose:
            print("DCC ID '{}' will be saved if the Flow initialization is successful "
                  "and this is not a dry run"
                  .format(dcc_id))
    try:
        if verbose:
            print("Initializing Flow")
        cfde = CfdeClient(no_browser=no_browser, force=force_login,
                          service_instance=service_instance)
        if verbose:
            print("CfdeClient initialized, starting Flow")
        start_res = cfde.start_deriva_flow(data_path, dcc_id=dcc_id, catalog_id=catalog,
                                           schema=schema, dataset_acls=dataset_acls,
                                           output_dir=output_dir, delete_dir=delete_dir,
                                           handle_git_repos=(not ignore_git),
                                           server=server, dry_run=dry_run,
                                           test_sub=test_submission, verbose=verbose,
                                           force_http=force_http, **bag_kwargs)
    except Exception as e:
        print("Error while starting Flow: {}".format(repr(e)))
        return
    else:
        if not start_res["success"]:
            print("Error during Flow startup: {}".format(start_res["error"]))
        else:
            print(start_res["message"])
            if not dry_run:
                state["service_instance"] = service_instance
                state["flow_id"] = start_res["flow_id"]
                state["flow_instance_id"] = start_res["flow_instance_id"]
                state["http_link"] = start_res["http_link"]
                state["globus_web_link"] = start_res["globus_web_link"]
                with open(client_state_file, 'w') as out:
                    json.dump(state, out)
                if verbose:
                    print("State saved to '{}'".format(client_state_file))

                filename = os.path.basename(start_res["cfde_dest_path"])
                print("\nThe BDBag with your data is named '{}', and will be available through "
                      "Globus here:\n{}\n".format(filename, state["globus_web_link"]))
                print("You BDBag will also be available via direct HTTP download here:\n{}"
                      .format(state["http_link"]))


@cli.command()
@click.option("--flow-id", default=None, show_default=True)
@click.option("--flow-instance-id", default=None, show_default=True)
@click.option("--raw", is_flag=True, default=False)
@click.option("--client-state-file", type=click.Path(exists=True), default=None)  # , hidden=True)
@click.option("--service-instance", default=None)  # , hidden=True)
def status(flow_id, flow_instance_id, raw, client_state_file, service_instance):
    """Check the status of a Flow."""
    if not flow_id or not flow_instance_id:
        if not client_state_file:
            client_state_file = DEFAULT_STATE_FILE
        try:
            with open(client_state_file) as f:
                client_state = json.load(f)
            flow_id = flow_id or client_state.get("flow_id")
            flow_instance_id = flow_instance_id or client_state.get("flow_instance_id")
            service_instance = service_instance or client_state.get("service_instance")
            if not flow_id or not flow_instance_id:
                raise ValueError("flow_id or flow_instance_id not found")
        except (FileNotFoundError, ValueError):
            print("Flow not started and flow-id or flow-instance-id not specified")
            return
    try:
        cfde = CfdeClient(service_instance=service_instance)
        status_res = cfde.check_status(flow_id, flow_instance_id, raw=True)
    except Exception as e:
        if raw:
            err = repr(e)
        else:
            err = str(e)
        print("Error checking status for Flow '{}': {}".format(flow_instance_id, err))
        return
    else:
        if raw:
            print(json.dumps(status_res, indent=4, sort_keys=True))
        else:
            print(status_res["clean_status"])


@cli.command()
@click.option("--force-login", is_flag=True, default=False, show_default=True)
@click.option("--no_browser", is_flag=True, default=False)
def login(force_login, no_browser):
    """Perform the login step (which saves credentials) by initializing
    a CfdeClient. The Client is then discarded.
    """
    print("Starting login check")
    CfdeClient(no_browser=no_browser, force=force_login)
    print("You are authenticated and your tokens have been cached.")


@cli.command()
def logout():
    """Log out and revoke your tokens."""
    print("Logging out and revoking tokens")
    # Messing with the tokens outside of the CfdeClient seems like an error-prone idea.
    # However, we don't have a Client instantiated here to log out with.
    # So, we're going to attempt to create one.
    try:
        # We'll suppress stdout, so the user isn't actually prompted to log in,
        # and prepare an invalid prompt response in stdin.
        old_stdin = sys.stdin
        new_stdin = StringIO("\n")
        sys.stdin = new_stdin
        # If the auth flow fires, it will read the invalid response and raise an exception,
        # which indicates that there are no valid existing tokens,
        # so the user is already logged out.
        old_stdout = sys.stdout
        with open(os.devnull, 'w') as new_stdout:
            sys.stdout = new_stdout
            client = CfdeClient(no_browser=True)
        # Otherwise, if the Client initializes without an auth step, we must actually logout.
        client.logout()
    except Exception as e:
        # If this is an invalid grant error, there are no valid existing tokens,
        # so we can eat the exception
        if len(e.args) >= 3 and e.args[2] == "invalid_grant":
            pass
        # Else, the exception was unexpected
        else:
            raise
    finally:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
    print("You are logged out.")
