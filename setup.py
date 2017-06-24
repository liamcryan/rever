import os
from setuptools import setup

#  a lot of this borrowed from requests structuring

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "rever", '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.rst', 'r') as f:
    readme = f.read()

with open('HISTORY.rst', 'r') as f:
    history = f.read()

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__description__"],
      long_description=readme + '\n\n' + history,
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      packages=[about["__title__"]],
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Programming Language :: Python 3",
                   "Programming Language :: Python 3.6"]
      )