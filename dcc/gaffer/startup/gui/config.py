# Archivo: /ruta/a/tu/pipeline/dcc/gaffer/startup/gui/config.py

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

        # 1.get  NameValuePlug (context variable)

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

        # 3. Bloquear la variable para que el artista no la cambie.
        Gaffer.MetadataAlgo.setReadOnly(root_dir_plug, True)
        Gaffer.MetadataAlgo.setReadOnly(project_name_plug, True)

    # Conectar señal: __scriptAdded se ejecuta cada vez que se abre un nuevo script (o al iniciar Gaffer)
    app_root["scripts"].childAddedSignal().connect(__scriptAdded)
    print("✅ Signal connected successfully.")

except NameError:
    # Esto ocurre si el script no está en la carpeta 'gui' o si se lanza en modo headless
    print(
        "❌ ERROR: Object 'application' not found. looking in folder of pipeline and dcc  /startup/gui/"
    )
except Exception as e:
    print(f"❌ CRITICAL ERROR  in config.py: {e}")

print("=" * 50 + "\n")
