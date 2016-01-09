import itertools
import os
import pathlib
import tempfile

import pytest

from fileperms import Permissions

class TestFromOctal:
    def test_valid(self):
        path = tempfile.mkstemp()[1]

        perms = '0 1 2 3 4 5 6 7'.split()
        perms = itertools.permutations(perms, 4)

        try:
            for item in perms:
                item = ''.join(item)
                os.chmod(path, int(item, 8))

                perm = Permissions.from_path(path)
                assert isinstance(perm, Permissions)
                assert perm.to_octal() == item

                path2 = pathlib.Path(path)
                perm = Permissions.from_path(path2)
                assert isinstance(perm, Permissions)
                assert perm.to_octal() == item
        finally:
            os.unlink(path)

    def test_non_existed_files(self):
        with pytest.raises(FileNotFoundError):
            Permissions.from_path('/qwe')

        with pytest.raises(FileNotFoundError):
            Permissions.from_path(pathlib.Path('/qwe'))

    def test_invalid_types(self):
        for value in (123, object(), b'rwxrwxrwx', True, None):
            with pytest.raises(TypeError):
                Permissions.from_path(value)
