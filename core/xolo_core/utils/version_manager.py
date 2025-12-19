import json
from pathlib import Path
import requests

GITLAB_API = "https://gitlab.com/api/v4"
PROJECT_PATH = "xololab/xolo-pipeline"

CACHE_FILE = Path(__file__).resolve().parent.parent / "version_cache.json"


def _project_id() -> str:
    """Encode project path for GitLab API."""
    return PROJECT_PATH.replace("/", "%2F")


def fetch_gitlab_version() -> str | None:
    """Fetch latest release tag from GitLab."""
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


def load_cached_version() -> str | None:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text()).get("version")
        except Exception:
            return None
    return None


def save_cached_version(version: str) -> None:
    CACHE_FILE.write_text(
        json.dumps({"version": version}, indent=2),
        encoding="utf-8",
    )


def get_version(force_refresh: bool = False) -> str:
    if not force_refresh:
        cached = load_cached_version()
        if cached:
            return cached

    latest = fetch_gitlab_version()
    if latest:
        save_cached_version(latest)
        return latest

    return load_cached_version() or "unknown"


def check_for_updates(current_version: str) -> str | None:
    latest = fetch_gitlab_version()
    if latest and latest != current_version:
        save_cached_version(latest)
        return latest
    return None
