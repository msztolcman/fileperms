"""
fileperms helps you read, change and set file permissions
"""

import enum
import os
import pathlib
import re
import stat

__version__ = '1.2.0'

from typing import Union


class Permission(enum.IntEnum):
    """
    Enum with available permissions
    """
    suid = stat.S_ISUID
    sgid = stat.S_ISGID
    sticky = stat.S_ISVTX

    owner_read = stat.S_IRUSR
    owner_write = stat.S_IWUSR
    owner_exec = stat.S_IXUSR

    group_read = stat.S_IRGRP
    group_write = stat.S_IWGRP
    group_exec = stat.S_IXGRP

    other_read = stat.S_IROTH
    other_write = stat.S_IWOTH
    other_exec = stat.S_IXOTH


# pylint: disable=too-many-instance-attributes
class Permissions:
    """
    Class that helps to manipulate permissions of file
    """
    RXP_FILEMODE = re.compile(r'^[r-][w-][xsS-][r-][w-][xsS-][r-][w-][xtT-]$')
    RXP_OCTAL = re.compile(r'^[0-7]{3,4}$')

    def __init__(self) -> None:
        self.suid = False
        self.sgid = False
        self.sticky = False
        self.owner_read = False
        self.owner_write = False
        self.owner_exec = False
        self.group_read = False
        self.group_write = False
        self.group_exec = False
        self.other_read = False
        self.other_write = False
        self.other_exec = False

    def set(self, perm: Permission, value: bool) -> 'Permissions':
        """
        Enable or disable permission
        :param perm:One of Permission item
        :param value:
        :return self:
        """
        if not isinstance(perm, Permission):
            raise ValueError(f"Invalid permission: {perm}. It should be an instance of Permission enum.")
        if not isinstance(value, bool):
            raise ValueError(f"Invalid value: {value}. It should be a boolean.")
        setattr(self, perm.name, value)
        return self

    def get(self, perm: Permission) -> bool:
        """
        Return value of permission
        :param perm:
        :return bool:
        """
        if not isinstance(perm, Permission):
            raise ValueError(f"Invalid permission: {perm}. It should be an instance of Permission enum.")
        return getattr(self, perm.name)

    @classmethod
    def from_path(cls, path: Union[str, pathlib.Path]) -> 'Permissions':
        """
        Read files permissions and create Permissions object with filled properties
        :param path:String or pathlib.Path
        :return:
        """
        if hasattr(path, 'lstat'):
            modes = path.lstat().st_mode
        elif hasattr(path, 'stat'):
            modes = path.stat(follow_symlinks=True).st_mode
        elif isinstance(path, str):
            modes = os.lstat(path).st_mode
        else:
            raise TypeError("path must be a string or had stat/lstat method (like pathlib.Path)")

        prm = cls()
        for mode in Permission:
            setattr(prm, mode.name, modes & mode == mode)

        return prm

    @classmethod
    def from_int(cls, perms: int) -> 'Permissions':
        """
        Create Permissions object, read permissions from int value
        :param perms:
        :return:
        """
        try:
            filemode = stat.filemode(perms)
        except OverflowError as exc:
            raise ValueError("Invalid value of permissions: %s" % perms) from exc

        if perms > 0o7777:
            raise ValueError("Invalid value of permissions: %s" % perms)

        # filemode = stat.filemode(perms)
        return cls.from_filemode(filemode)

    @classmethod
    def from_octal(cls, perms: str) -> 'Permissions':
        """
        Create Permissions object, read permissions from octal value
        :param perms:
        :return:
        """
        if not cls.RXP_OCTAL.match(perms):
            raise ValueError("Invalid format of permissions: %s" % perms)
        if len(perms) == 3:
            perms = '0' + perms
        perms = int(perms, 8)
        return cls.from_int(perms)

    @classmethod
    def from_filemode(cls, perms: str) -> 'Permissions':
        """
        Create Permissions object, read permissions from string in format: rwxrwxrwx
        :param perms:
        :return:
        """

        # trim optional 'type' from file mode (d, - or similar from 'drwxrwxrwx')
        if len(perms) == 10:
            perms = perms[1:]

        if not cls.RXP_FILEMODE.match(perms):
            raise ValueError("Incorrect format of permissions: %s" % perms)

        prm = cls()
        prm.owner_read = perms[0] == 'r'
        prm.owner_write = perms[1] == 'w'
        prm.owner_exec = perms[2] in 'xs'
        prm.suid = perms[2] in 'sS'

        prm.group_read = perms[3] == 'r'
        prm.group_write = perms[4] == 'w'
        prm.group_exec = perms[5] in 'xs'
        prm.sgid = perms[5] in 'sS'

        prm.other_read = perms[6] == 'r'
        prm.other_write = perms[7] == 'w'
        prm.other_exec = perms[8] in 'xt'
        prm.sticky = perms[8] in 'tT'

        return prm

    def to_octal(self) -> str:
        """
        Dump Permissions to octal format
        :return:
        """
        octal = (
            str(
                (0 if not self.suid else 4) |
                (0 if not self.sgid else 2) |
                (0 if not self.sticky else 1)
            ),
            str(
                (0 if not self.owner_read else 4) |
                (0 if not self.owner_write else 2) |
                (0 if not self.owner_exec else 1)
            ),
            str(
                (0 if not self.group_read else 4) |
                (0 if not self.group_write else 2) |
                (0 if not self.group_exec else 1)
            ),
            str(
                (0 if not self.other_read else 4) |
                (0 if not self.other_write else 2) |
                (0 if not self.other_exec else 1)
            ),
        )

        # pylint: disable=redefined-variable-type
        octal = ''.join(octal)

        return octal

    def to_int(self) -> int:
        """
        Dump Permissions to int format
        :return:
        """
        octal = self.to_octal()
        return int(octal, 8)

    def to_filemode(self) -> str:
        """
        Dump Permissions to filemode format
        :return:
        """
        return stat.filemode(self.to_int())[1:]

    def apply(self, path: Union[str, pathlib.Path]) -> 'Permissions':
        """
        Apply Permissions to given path
        :param path:
        :return self:
        """
        if hasattr(path, 'chmod'):
            path.chmod(int(self))
        elif isinstance(path, str):
            os.chmod(path, int(self))
        else:
            raise TypeError("path must be a string or had chmod method (like pathlib.Path)")

        return self

    __str__ = to_octal
    __int__ = to_int

    def __repr__(self) -> str:
        return '<Permissions(%s)>' % self


def from_path(path: Union[pathlib.Path, str]) -> Permissions:
    """Create Permissions instance reading permissions from path.

    Shortcut for Permissions.from_path()
    """
    return Permissions.from_path(path)


def from_int(perms: int) -> Permissions:
    """Create Permissions instance reading permissions from integer value.

    Shortcut for Permissions.from_int()
    """
    return Permissions.from_int(perms)


def from_octal(perms: str) -> Permissions:
    """Create Permissions instance reading permissions from octal value.

    Shortcut for Permissions.from_oct()
    """
    return Permissions.from_octal(perms)


def from_filemode(perms: str) -> Permissions:
    """Create Permissions instance reading permissions from string in format: rwxrwxrwx.

    Shortcut for Permissions.from_filemode()
    """
    return Permissions.from_filemode(perms)
