import tempfile, os, zipfile, shutil
from utils.safe_extract import safe_extract_zip

def test_safe_extract_normal(tmp_path):
    zf_path = tmp_path / "sample.zip"
    target = tmp_path / "out"
    with zipfile.ZipFile(zf_path, "w") as zf:
        zf.writestr("file.txt", "hello")
    safe_extract_zip(str(zf_path), str(target))
    assert (target / "file.txt").exists()

def test_safe_extract_traversal(tmp_path):
    zf_path = tmp_path / "evil.zip"
    with zipfile.ZipFile(zf_path, "w") as zf:
        zf.writestr("../evil.txt", "x")
    try:
        safe_extract_zip(str(zf_path), str(tmp_path / "out"))
        assert False, "Should have raised for traversal"
    except Exception:
        pass
