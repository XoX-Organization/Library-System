import sys
from setuptools import setup, find_packages

with open("README.md", "r") as README :
    LongDescription = README.read()

setup(
    name = "LibrarySystem",
    version = "0.0.0",
    description = "School Assignment",
    author = "Xian Yee",
    author_email = "2003victoryy@1utar.my",
    url = "https://github.com/victoryy2003/Library-System",
    packages = find_packages (exclude = ["tests"]),
    zip_safe = False,
    python_requires = ">=2.0.0",
    install_requires = [
        "tabulate"
        ],
    entry_points = {
        "console_scripts": ["LibSys = LibSys.main:main"],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    long_description = LongDescription,
    long_description_content_type = "text/markdown",
)
