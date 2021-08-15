#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="doc-log",
    version="0.1.0",
    description="Smarter logging based on Python docstrings.",
    author="Jacob Wahlman <mr.jacobwahlman+git@gmail.com>",
    url="https://github.com/wahl-sec/doc-log",
    packages=["doc_log"],
    extras_require={"dev": ["black>=21.7b0 ", "pytest>=6.2.4"]},
)
