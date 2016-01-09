import itertools
import pytest

from fileperms import Permissions

class TestFromOctal:
    def test_valid(self):
        perms = '0 1 2 3 4 5 6 7'.split()

        perms = itertools.product(perms, perms, perms, perms)
        for item in perms:
            item = ''.join(item)
            assert len(item) == 4

            perm = Permissions.from_octal(item)

            assert isinstance(perm, Permissions)
            assert perm.to_octal() == item

            item = item[1:]

            perm = Permissions.from_octal(item)

            assert isinstance(perm, Permissions)
            assert perm.to_octal() == '0' + item

    def test_invalid_types(self):
        for value in ('a', 123, object(), b'rwxrwxrwx', True, None):
            with pytest.raises((TypeError, ValueError)):
                Permissions.from_octal(value)

    def test_bad_input(self):
        perms_org = '0777'
        for i, _ in enumerate(perms_org):
            perms = perms_org[0:i] + 'a' + perms_org[i+1:]
            with pytest.raises(ValueError):
                Permissions.from_octal(perms)

        with pytest.raises(ValueError):
            Permissions.from_octal(perms_org[:-2])

        with pytest.raises(ValueError):
            Permissions.from_octal(perms_org + 'x')

        with pytest.raises(ValueError):
            Permissions.from_octal('')
