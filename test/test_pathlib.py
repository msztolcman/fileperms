import itertools
import os
import pathlib
import stat
import tempfile

from fileperms import Permissions


class TestPathlib:
    def test(self):
        perms = '0 1 2 3 4 5 6 7'.split()
        path = pathlib.Path(tempfile.mkstemp()[1])

        try:
            perms = itertools.product(perms, perms, perms, perms)
            for item in perms:
                item = ''.join(item)
                assert len(item) == 4

                prm = Permissions.from_octal(item)
                path.lchmod(prm)

                assert stat.filemode(path.lstat().st_mode)[1:] == prm.to_filemode()
        finally:
            path.unlink()
