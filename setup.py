#!/usr/bin/env python

import os
import sys

from setuptools import find_packages, setup

exec(open("fsutil/metadata.py").read())

github_url = "https://github.com/fabiocaccamo"
sponsor_url = "https://github.com/sponsors/fabiocaccamo/"
twitter_url = "https://twitter.com/fabiocaccamo"
package_name = "python-fsutil"
package_url = "{}/{}".format(github_url, package_name)
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, "README.md")
long_description_content_type = "text/markdown"
long_description = ""
try:
    with open(long_description_file_path, "r", encoding="utf-8") as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name=package_name,
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author=__author__,
    author_email=__email__,
    url=package_url,
    download_url="{}/archive/{}.tar.gz".format(package_url, __version__),
    project_urls={
        "Documentation": "{}#readme".format(package_url),
        "Issues": "{}/issues".format(package_url),
        "Funding": sponsor_url,
        "Twitter": twitter_url,
    },
    keywords=[
        "python",
        "file",
        "system",
        "util",
        "utils",
        "utility",
        "utilities",
        "dir",
        "directory",
        "path",
        "fs",
        "os",
        "shutil",
        "glob",
    ],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment :: File Managers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    license=__license__,
    test_suite="tests",
)
