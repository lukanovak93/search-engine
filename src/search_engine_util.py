import os

def _get_files(base_dir):
    for entry in os.scandir(base_dir):
        if entry.is_file():
            yield entry.path
        elif entry.is_dir():
            yield from _get_files(entry.path)
