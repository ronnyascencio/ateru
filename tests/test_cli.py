# tests/test_cli.py
from typer.testing import CliRunner

from src.xolo.cli.python.main import app

runner = CliRunner()


def test_settings_show():
    result = runner.invoke(app, ["settings", "show"])
    assert result.exit_code == 0
    assert "Pipeline Configuration" in result.output
