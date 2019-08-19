import os
from functools import lru_cache

"""
    Types of path

    FS paths: `fpath`, `fn`, `filename`, `*dir`
     - Canonical or relative to working directory
     - Valid if used with open(), for example
     - Never end in /
     - Only begin with / if canonical

    Resource paths: `rpath`
     - Never begin with /
     - Always relative to base directory
     - Valid if passed to os.path.join(basedir, ... )
     - Ends with / <=> refers to folder

"""

@lru_cache(maxsize=1000)
def get_fs_path(basedir : str, rpath : str):
    assert not rpath.startswith("/"), "rpath cannot start with /"
    return os.path.join(basedir, rpath)

@lru_cache(maxsize=1000)
def get_resource_path(basedir : str, fpath : str):
    assert not fpath.endswith("/"), "fpath cannot end with /"
    relpath = os.path.relpath(fpath, basedir)
    if relpath == os.path.curdir: return ""
    if os.path.pardir in relpath.split(os.path.pathsep):
        print(fpath)
        print(relpath)
        raise FileNotFoundError("fpath is not under basedir")
    else: return relpath