import itertools
import pytest

from fileperms import Permissions

class TestFromInt:
    def test_valid(self):
        perms = '0 1 2 3 4 5 6 7'.split()

        perms = itertools.permutations(perms, 4)
        for item in perms:
            item = ''.join(item)
            assert len(item) == 4

            item_int = int(item, 8)

            perm = Permissions.from_int(item_int)

            assert isinstance(perm, Permissions)
            assert perm.to_octal() == item

            item = item[1:]

            perm = Permissions.from_octal(item)

            assert isinstance(perm, Permissions)
            assert perm.to_octal() == '0' + item

    def test_invalid_types(self):
        for value in ('a', object(), b'rwxrwxrwx', None):
            try:
                Permissions.from_int(value)
                assert False, "Value \"%s\" (type: %s) do not fail" % (value, type(value))
            except TypeError:
                pass

    def test_bad_input(self):
        for value in (int('7777', 8) + 1, ):
            with pytest.raises(ValueError):
                Permissions.from_int(value)
