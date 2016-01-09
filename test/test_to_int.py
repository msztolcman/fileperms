import itertools
import stat

import pytest

from fileperms import Permissions, Permission

class TestToInt:
    def test_mutated(self):
        perm = Permissions()

        assert perm.to_int() == 0

        expected_int = 0
        for item in Permission:
            perm.set(item, True)

            expected_int = expected_int | item
            assert perm.to_int() == expected_int

    def test_immutated(self):
        for item in Permission:
            perm = Permissions()
            perm.set(item, True)
            assert perm.to_int() == int(item)
