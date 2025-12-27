"""Global variables configuration for Gaffer scripts"""

import os

import Gaffer

from core.xolo_core.utils.logging import log_core, log_error, log_ui

log_core("GAFFER CUSTOM STARTUP: loading  config.py...")
log_core("Looking for PROJECT_ROOT in environment...")

try:
    app_root = application.root()

    def __scriptAdded(container, script):
        log_core(f" Configuring script: {script.getName()}")

        variables = script["variables"]
        project_root = os.environ.get("XOLO_PROJECT_ROOT")
        project_name = str(project_root).split("/")[-1]

        if not project_root:
            log_error(" XOLO_PROJECT_ROOT env var not found!")
            return

        """ get  NameValuePlug (context variable)"""

        root_dir_plug = variables["projectRootDirectory"]
        project_name_plug = variables["projectName"]

        """ set variable values"""
        root_dir_plug["value"].setValue(project_root)
        project_name_plug["value"].setValue(project_name)

        log_core(
            f" Variable set: project:rootDirectory -> {root_dir_plug['value'].getValue()}"
        )
        log_core(
            f" Variable set: project:projectName -> {project_name_plug['value'].getValue()}"
        )

        """ blocking variable editing"""
        Gaffer.MetadataAlgo.setReadOnly(root_dir_plug, True)
        Gaffer.MetadataAlgo.setReadOnly(project_name_plug, True)

    """ signal connection: __scriptAdded it runs when gaffer starts"""
    app_root["scripts"].childAddedSignal().connect(__scriptAdded)
    log_core(" Signal connected successfully.")

except NameError:
    """ handle if there is no script in gui directory"""
    log_error(
        "Object 'application' not found. looking in folder of pipeline and dcc  /startup/gui/"
    )
except Exception as e:
    log_error(f"CRITICAL in config.py: {e}")
