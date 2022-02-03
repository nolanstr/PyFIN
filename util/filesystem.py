import os
from contextlib import contextmanager


@contextmanager
def working_dir(dirname):
    old_cwd = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(old_cwd)
