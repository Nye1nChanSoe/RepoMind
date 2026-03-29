from pathlib import Path

from core.ingestion import is_supported_file, walk_files


def test_walk_files_skips_noise_directories(tmp_path: Path) -> None:
    src_dir = tmp_path / "src"
    ignored_dir = tmp_path / "node_modules"
    src_dir.mkdir()
    ignored_dir.mkdir()

    app_file = src_dir / "app.py"
    vendor_file = ignored_dir / "vendor.py"
    app_file.write_text("print('hello')\n", encoding="utf-8")
    vendor_file.write_text("print('ignore')\n", encoding="utf-8")

    files = walk_files(str(tmp_path))

    assert str(app_file) in files
    assert str(vendor_file) not in files


def test_is_supported_file_rejects_large_files(tmp_path: Path) -> None:
    large_file = tmp_path / "large.py"
    large_file.write_text("x" * 2048, encoding="utf-8")

    assert not is_supported_file(str(large_file), max_file_size_kb=1)
