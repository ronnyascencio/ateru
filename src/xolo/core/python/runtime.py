from importlib.metadata import PackageNotFoundError, version


def app_version() -> str:
    """
    Return installed Xolo Pipeline version.
    Source of truth: package metadata (pyproject.toml).
    """
    try:
        return version("xolo-pipeline")
    except PackageNotFoundError:
        # Editable / dev mode
        return "dev"
