import requests

GITLAB_API = "https://gitlab.com/api/v4"
PROJECT_PATH = "xololab/xolo-pipeline"


def _project_id() -> str:
    return PROJECT_PATH.replace("/", "%2F")


def fetch_gitlab_version() -> str | None:
    """
    Fetch latest GitLab release version (without leading 'v').
    """
    try:
        url = f"{GITLAB_API}/projects/{_project_id()}/releases"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        releases = response.json()
        if not releases:
            return None

        tag = releases[0].get("tag_name")
        return tag.lstrip("v") if tag else None

    except Exception:
        return None
