def format_project_info(info: dict[str, object]) -> str:
    lines = [
        "",
        " Project Information",
        "----------------------",
        f"ID           : {info.get('id')}",
        f"Project Name : {info.get('name')}",
        f"FPS          : {info.get('fps')}",
        f"Resolution   : {info.get('resolution')}",
        f"Root Path    : {info.get('root_path')}",
        f"USD Path     : {info.get('usd_root')}",
        f"Assets Path  : {info.get('assets_path')}",
        f"OCIO Config  : {info.get('ocio_path')}",
    ]
    return "\n".join(lines)
