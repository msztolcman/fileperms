import itertools
import pytest

from fileperms import Permissions

class TestFromFilemode:
    def test_valid(self):
        perms = (
            ('-r', '-w', '-xsS'),
            ('-r', '-w', '-xsS'),
            ('-r', '-w', '-xtT'),
        )

        perms = itertools.product(*perms[0], *perms[1], *perms[2])
        for item in perms:
            item = ''.join(item)
            assert len(item) == 9

            perm = Permissions.from_filemode(item)

            assert isinstance(perm, Permissions)
            assert perm.to_filemode() == item

    def test_invalid_types(self):
        for value in (123, object(), b'rwxrwxrwx', True, None):
            with pytest.raises(TypeError):
                Permissions.from_filemode(value)

    def test_bad_input(self):
        perms_org = 'rwxrwxrwx'
        for i, _ in enumerate(perms_org):
            perms = perms_org[0:i] + '1' + perms_org[i+1:]
            with pytest.raises(ValueError):
                Permissions.from_filemode(perms)

        with pytest.raises(ValueError):
            Permissions.from_filemode(perms_org[:-1])

        with pytest.raises(ValueError):
            Permissions.from_filemode(perms_org + 'x')

        with pytest.raises(ValueError):
            Permissions.from_filemode('')
