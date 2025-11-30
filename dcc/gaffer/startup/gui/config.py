# Global variables configuration for Gaffer scripts
import os

import Gaffer
import IECore

# Print Debug Info
print("\n" + "=" * 50)
print("GAFFER CUSTOM STARTUP: loading  config.py...")
print("Looking for PROJECT_ROOT in environment...")

try:
    app_root = application.root()

    def __scriptAdded(container, script):
        print(f"⚙️  Configuring script: {script.getName()}")

        variables = script["variables"]
        project_root = os.environ.get("PROJECT_ROOT")
        project_name = project_root.split("/")[-1]

        if not project_root:
            print("❌ ERROR: PROJECT_ROOT env var not found!")
            return

        # get  NameValuePlug (context variable)

        root_dir_plug = variables["projectRootDirectory"]
        project_name_plug = variables["projectName"]

        # set variable values
        root_dir_plug["value"].setValue(project_root)
        project_name_plug["value"].setValue(project_name)

        print(
            f"✅ Variable set: project:rootDirectory -> {root_dir_plug['value'].getValue()}"
        )
        print(
            f"✅ Variable set: project:projectName -> {project_name_plug['value'].getValue()}"
        )

        # blocking variable editing
        Gaffer.MetadataAlgo.setReadOnly(root_dir_plug, True)
        Gaffer.MetadataAlgo.setReadOnly(project_name_plug, True)

    # signal connection: __scriptAdded it runs when gaffer starts
    app_root["scripts"].childAddedSignal().connect(__scriptAdded)
    print("✅ Signal connected successfully.")

except NameError:
    # handle if there is no script in gui directory
    print(
        "❌ ERROR: Object 'application' not found. looking in folder of pipeline and dcc  /startup/gui/"
    )
except Exception as e:
    print(f"❌ CRITICAL ERROR  in config.py: {e}")

print("=" * 50 + "\n")
