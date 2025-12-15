import yaml
from pathlib import Path


yaml_path = Path(__file__).parent / "utils" / "dcc_map.yml"

def load_map(dcc: str):
    # load YAML
    with open(yaml_path, "r") as f:
        dcc_map = yaml.safe_load(f)  # esto será un dict

    # check if exists
    if dcc not in dcc_map:
        return "DCC not supported"

    # load the list of the formats
    formats = dcc_map["software"][dcc]["format"]
    return formats
