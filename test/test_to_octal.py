import itertools
import stat

import pytest

from fileperms import Permissions, Permission

class TestToOctal:
    def _to_oct(self, val):
        val = oct(val)[2:]
        val = '0o%04d' % int(val)
        return val

    def test_mutated(self):
        perm = Permissions()

        assert perm.to_octal() == '0000'

        expected_int = 0
        for item in Permission:
            perm.set(item, True)

            expected_int = expected_int | item
            assert '0o' + perm.to_octal() == self._to_oct(expected_int)

    def test_immutated(self):
        for item in Permission:
            perm = Permissions()
            perm.set(item, True)

            assert '0o' + perm.to_octal() == self._to_oct(item)
