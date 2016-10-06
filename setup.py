import pkg_resources
import platform
import sys


def validate_python_version():
    """
    Validate python interpreter version. Only 3.3+ allowed.
    """
    if pkg_resources.parse_version(platform.python_version()) < pkg_resources.parse_version('3.3.0'):
        print("Sorry, Python 3.3+ is required")
        sys.exit(1)
validate_python_version()


from codecs import open
from os import path
from setuptools import setup, find_packages

BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fileperms',
    version='1.0.4',
    description='fileperms is small library for describing file permissions',
    long_description=long_description,
    url='http://msztolcman.github.io/fileperms/',
    author='Marcin Sztolcman',
    author_email='marcin@urzenia.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Filesystems',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[],
    packages=find_packages(),

    keywords='files permissions posix',
)

