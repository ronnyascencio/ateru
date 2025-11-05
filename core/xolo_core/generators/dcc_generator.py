from pathlib import Path
import yaml
import os
from core.xolo_core.extractors.system_extractor import get_os_type


def get_system_root() -> Path:
    """root acording OS"""
    try:
        os_type = get_os_type().lower()
        if os_type == "windows":
            root = Path(Path.home().drive + "\\")
        elif os_type == "darwin":
            root = Path("/Aplications")
        elif os_type == "linux":
            root = Path("/opt")
        return root

    except Exception as e:
        print(f"⚠️ Error obtaining system root: {e}")
        return Path.home()


def dcc_finder_root(dcc_name: str):
    """get the list of directorys to search in for get dcc name"""
    root_path = get_system_root()

    dcc_name = dcc_name

    list = os.listdir(root_path)
    for name in list:
        if name.startswith(dcc_name):
            print(name)

    print(list)


def dcc_root_path(dcc_name: str):
    pipeline_path = Path(__file__).parent.parent.parent.parent.resolve()
    config_path = Path(pipeline_path, "dcc/config.yml").resolve()
    # print(config_path)
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    dccs = data.get("dcc")
    dcc_name = dcc_name
    dcc_version = dccs[dcc_name]
    version = dcc_version.get("default")

    if dcc_name == "nuke":
        exce_name = str(dcc_name.title() + version)
        dcc_compile = Path(get_system_root(), "nuke/", exce_name)
    elif dcc_name == "gaffer":
        dcc_compile = Path(get_system_root(), dcc_name, version, "bin", dcc_name)
    elif dcc_name == "blender":
        dcc_compile = Path(get_system_root(), dcc_name, version, dcc_name)

    return Path(dcc_compile)


print(dcc_root_path("gaffer"))
