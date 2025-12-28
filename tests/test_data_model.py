from pathlib import Path


def test_project_model_creation(tmp_path):
    from src.xolo.core.python.models.project import Project

    project = Project(
        name="reel",
        resolution=(1920, 1080),
        usd_root=tmp_path,
        ocio_path=str(tmp_path),
        root_path=tmp_path,
        fps=24,
        assets_path=tmp_path,
    )

    assert project.fps == 24
    assert project.resolution == (1920, 1080)

    assert Path(project.ocio_path) == tmp_path
