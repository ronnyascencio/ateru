def test_project_model_creation(tmp_path):
    from core.xolo_core.models.project import Project
    tmp_path = str(tmp_path)

    project = Project(
        name="reel",
        root=tmp_path,
        resolution=(1920,1080),
        usd_root=tmp_path,
        OCIO_path=tmp_path,
        root_path=tmp_path,
        fps=24
    )

    assert project.fps == 24
    assert project.resolution == (1920, 1080)
    assert project.usd_root == tmp_path
    assert project.OCIO_path == tmp_path
    assert project.root_path == tmp_path
    assert project.name == "reel"
