"""
A setup.py file based on the kennethreitz/setup.py on GitHub.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'mgl2d'
DESCRIPTION = 'Simple 2D game library using PySDL2 and modern OpenGL'
LONGDESCRIPTION = 'See the README.md file on GitHub for more information.'
URL = 'https://github.com/maxfish/mgl2d'
EMAIL = 'massimiliano.pesce@gmail.com'
AUTHOR = 'Massimiliano Pesce'
VERSION = '0.9.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'numpy == 1.13.0',
    'Pillow == 4.1.1',
    'PyOpenGL == 3.1.0',
    'PySDL2 == 0.9.6',
    'PyTMX == 3.21.1'
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath('pypi/')


class UploadCommand(Command):
    """Support setup.py upload."""
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        """Initialization options."""
        pass

    def finalize_options(self):
        """Finalize options."""
        pass

    def run(self):
        """Remove previous builds."""
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel distribution...')
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONGDESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list at https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
