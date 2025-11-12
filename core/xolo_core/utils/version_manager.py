import json
from pathlib import Path

import requests

REPO = "xololab/xolo-pipeline"
CACHE_FILE = Path(__file__).resolve().parent.parent / "version_cache.json"


def fetch_github_version() -> str | None:
    """Fetch the latest release tag from GitHub (public repo)."""
    try:
        url = f"https://api.github.com/repos/{REPO}/releases/latest"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        tag = data.get("tag_name")
        return tag.lstrip("v") if tag else None
    except Exception:
        return None


def load_cached_version() -> str | None:
    """Read version from local cache file."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("version")
        except Exception:
            return None
    return None


def save_cached_version(version: str) -> None:
    """Save version to local cache file."""
    CACHE_FILE.write_text(json.dumps({"version": version}, indent=2), encoding="utf-8")


def get_version(force_refresh: bool = False) -> str:
    """
    Always try to fetch GitHub version.
    If it fails, fallback to cached version.
    """
    if not force_refresh:
        # First check cache (fast path)
        cached = load_cached_version()
        if cached:
            return cached

    latest = fetch_github_version()
    if latest:
        save_cached_version(latest)
        return latest
    return load_cached_version() or "unknown"


def check_for_updates(current_version: str) -> str | None:
    """Check if a newer release is available."""
    latest = fetch_github_version()
    if latest and latest != current_version:
        save_cached_version(latest)
        return latest
    return None
