#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="doc-log",
    version="0.1.0",
    author="Jacob Wahlman",
    author_email="mr.jacobwahlman+git@gmail.com",
    description="Smarter logging based on Python docstrings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wahl-sec/doc-log",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Documentation",
        "Topic :: Software Development :: Libraries",
    ],
    packages=["doc_log"],
    extras_require={"dev": ["black>=21.7b0 ", "pytest>=6.2.4"]},
    python_requires=">=3.7"
)
