#!/usr/bin/env python

from distutils.core import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='sphinx_ext_substitution',
      version='0.1.dev0',
      description='Sphinx extension for substituting variables',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      url="https://github.com/NordicHPC/sphinx_ext_substitution",
      author='Richard Darst',
      author_email='rkd@zgib.net',
      packages=['sphinx_ext_substitution'],
  )
