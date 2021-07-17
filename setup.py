from setuptools import setup, find_packages

import ciprs_reader

setup(name="ciprs_reader", install_requires=["lark-parser"], version=ciprs_reader.VERSION, packages=find_packages())
