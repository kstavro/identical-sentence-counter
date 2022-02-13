#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Konstantinos Stavropoulos <k.stavropoulos@oxolo.com>
# For License information, see corresponding LICENSE file.

import os

from setuptools import setup


# from setuptools import find_packages


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


PACKAGES = ["sentence_counter"]

PACKAGE_DATA = {
    "sentence_counter": package_files("sentence_counter"),
}

setup(
    name="sentence_counter",
    version="0.0.1",
    author="Konstantinos Stavropoulos",
    author_email="konstantinos.stavrop@fmail.com",
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    requires_python=">=3.8",
    install_requires=[],
)
