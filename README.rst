fileperms
=========

``fileperms`` is small library for describing file permissions.

Current stable version
----------------------

1.0.0

Features
--------

-  easy manipulating of permissions
-  works fine with ``os.chmod`` and ``pathlib.Path``

Python version
--------------

``fileperms`` works only with Python 3.3+. Older Python versions are
unsupported.

Some examples
-------------

::

    >>> import fileperms
    >>> fileperms.Permissions.from_path('/etc')
    <Permissions(0755)>
      
    >>> import os, stat
    >>> print(stat.filemode(os.stat(path).st_mode))
    -rw-------
    >>> prm = fileperms.Permissions.from_path(path)
    >>> prm
    <Permissions(0600)>
    >>> prm.to_filemode()
    'rw-------'
    >>> prm.owner_exec = True
    >>> prm.other_exec = True
    >>> os.chmod(path, prm)
    >>> print(stat.filemode(os.stat(path).st_mode))
    -rwx-----x

    >>> import pathlib
    >>> path = pathlib.Path(path)
    >>> prm.group_read = True
    >>> prm.group_write = True
    >>> path.chmod(prm)
    >>> print(stat.filemode(path.stat().st_mode))
    -rwxrw---x

Installation
------------

1. Using PIP

``fileperms`` should work on any platform where
`Python <http://python.org>`__ is available, it means Linux, Windows,
MacOS X etc, but is not tested on Windows.

Simplest way is to use Python's built-in package system:

::

    pip3 install fileperms

2. Using sources

Download sources from
`Github <https://github.com/msztolcman/fileperms/archive/1.0.0.zip>`__:

::

    wget -O 1.0.0.zip https://github.com/msztolcman/fileperms/archive/1.0.0.zip

or

::

    curl -o 1.0.0.zip https://github.com/msztolcman/fileperms/archive/1.0.0.zip

Unpack:

::

    unzip 1.0.0.zip

And install

::

    cd fileperms-1.0.0
    python3 setup.py install

Voila!

Authors
-------

Marcin Sztolcman marcin@urzenia.net

Contact
-------

If you like or dislike this software, please do not hesitate to tell me
about this me via email (marcin@urzenia.net).

If you find bug or have an idea to enhance this tool, please use
GitHub's `issues <https://github.com/msztolcman/fileperms/issues>`__.

License
-------

The MIT License (MIT)

Copyright (c) 2016 Marcin Sztolcman

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

ChangeLog
---------

v1.0.0
~~~~~~

-  first public version
