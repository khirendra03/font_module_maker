"""
safe_extract.py

Provides a safe routine to extract zip archives (defends against zip-slip/path traversal).
"""
import os
import zipfile

def safe_extract_zip(zip_path, target_dir, max_files=1000, max_size=200*1024*1024):
    """
    Safely extract zip file to target_dir.
    - Prevents path traversal (zip-slip).
    - Enforces limits on number of files and total uncompressed size (approximate).
    """
    target_dir = os.path.abspath(target_dir)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()
        if len(namelist) > max_files:
            raise ValueError(f"Archive has too many files: {len(namelist)} > {max_files}")
        total_uncompressed = 0
        for member in namelist:
            # Normalize path and prevent traversal
            dest = os.path.normpath(os.path.join(target_dir, member))
            if not dest.startswith(target_dir + os.sep) and dest != target_dir:
                raise Exception(f"Unsafe archive member detected: {member}")
            info = zf.getinfo(member)
            total_uncompressed += info.file_size
            if total_uncompressed > max_size:
                raise ValueError("Archive uncompressed size exceeds allowed limit")
        zf.extractall(target_dir)
