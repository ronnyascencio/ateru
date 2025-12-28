from src.xolo.core.python.runtime import app_version
from src.xolo.core.python.utils.version_manager import fetch_gitlab_version


def has_update() -> tuple[bool, str | None]:
    """
    Compare local version vs latest GitLab release.
    """
    current = app_version()
    latest = fetch_gitlab_version()

    if not latest:
        return False, None

    if current in ("dev", "unknown"):
        return False, None

    return latest != current, latest
