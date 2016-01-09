import itertools
import stat

import pytest

from fileperms import Permissions, Permission

class TestToFilemode:
    def test_mutated(self):
        perm = Permissions()

        assert perm.to_filemode() == '---------'

        expected_int = 0
        for item in Permission:
            perm.set(item, True)

            expected_int = expected_int | item
            assert perm.to_filemode() == stat.filemode(expected_int)[1:]

    def test_immutated(self):
        for item in Permission:
            perm = Permissions()
            perm.set(item, True)
            assert perm.to_filemode() == stat.filemode(item)[1:]
