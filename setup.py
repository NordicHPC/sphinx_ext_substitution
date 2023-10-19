#!/usr/bin/env python

from os.path import dirname, join
import setuptools


with open("README.rst", "r") as fh:
    long_description = fh.read()

requirementstxt = join(dirname(__file__), "requirements.txt")
requirements = [ line.strip() for line in open(requirementstxt, "r") if line.strip() ]

version_ns = { }
exec(open('sphinx_ext_substitution/_version.py').read(), version_ns)
version = version_ns['__version__']

setuptools.setup(name='sphinx_ext_substitution',
      version=version,
      description='Sphinx extension for substituting variables',
      long_description=long_description,
      long_description_content_type="text/x-rst",  # ReST is the default
      url="https://github.com/NordicHPC/sphinx_ext_substitution",
      author='Richard Darst',
      #author_email='',
      packages=['sphinx_ext_substitution'],
      package_data={
          "sphinx_ext_substitution": ['_static/*'],
          },
      keywords='sphinx-extension',
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*,",
      install_requires=requirements,
      classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Extension",
        "Operating System :: OS Independent",
    ],
  )

# python setup.py sdist bdist_wheel
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# twine upload dist/*
