import os
from setuptools import setup
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "rever", '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', 'r', 'utf-8') as f:
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
      keywords="retry decorator rever spanish",
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Programming Language :: Python 3",
                   "Programming Language :: Python 3.5"]
      )
