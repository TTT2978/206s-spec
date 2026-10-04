import os
import subprocess
import tempfile


def edit_with_nano(prompt=None):
    if prompt:
        print(prompt)
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    try:
        subprocess.call(["nano", path])
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    finally:
        os.remove(path)
    return content
