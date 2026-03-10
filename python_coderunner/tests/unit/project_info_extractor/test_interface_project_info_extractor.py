from pathlib import Path

from src.project_info_extractor import IProjectInfoExtractor


class TestProjectInfoExtractorInterface:
    def test_get_all_files_filter_by_exts(self, fixture_project_info_extractor: IProjectInfoExtractor) -> None:
        workspace_root: Path = Path(fixture_project_info_extractor.get_workspace_root())

        test_files: tuple[Path, ...] = (
            workspace_root / "file_0.py",
            workspace_root / "file_0.txt",
            workspace_root / "file_1.py",
            workspace_root / "dir_0" / "file_1.py",
            workspace_root / "dir_0" / "py.py",
        )

        for file_path in test_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)

        exts: set[str] = {".py", ".md"}
        result: set[Path] = {Path(p) for p in fixture_project_info_extractor.get_all_files_filter_by_exts(exts)}
        assert result == {
            workspace_root / "file_0.py",
            workspace_root / "file_1.py",
            workspace_root / "dir_0" / "file_1.py",
            workspace_root / "dir_0" / "py.py",
        }

    def test_get_all_files_filter_by_file_type(self, fixture_project_info_extractor: IProjectInfoExtractor) -> None:
        workspace_root: Path = Path(fixture_project_info_extractor.get_workspace_root())

        test_files: tuple[Path, ...] = (
            workspace_root / "file_0.py",
            workspace_root / "file_0.cpp",
            workspace_root / "file_0.txt",
            workspace_root / "file_1.py",
            workspace_root / "dir_0" / "file_1.py",
            workspace_root / "dir_0" / "py.py",
        )

        for file_path in test_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)

        file_types: set[str] = {"python", "cpp", "cobol"}
        result: set[Path] = {
            Path(p) for p in fixture_project_info_extractor.get_all_files_filter_by_file_type(file_types)
        }
        assert result == {
            workspace_root / "file_0.py",
            workspace_root / "file_0.cpp",
            workspace_root / "file_1.py",
            workspace_root / "dir_0" / "file_1.py",
            workspace_root / "dir_0" / "py.py",
        }
