#from distutils.core import setup #changed to distutils.core for pypy comptibility
from setuptools import setup
import sys

setup(
   name = "Pyevolve",
   version = '0.6',
   packages = ["pyevolve"],
   scripts = ['pyevolve_graph.py'],
   install_requires = ['future'],
   package_data = {
      'pyevolve': ['*.txt']
   },
   test_suite = 'tests',
   author = 'Christian S. Perone',
   author_email = "christian.perone@gmail.com",
   description = "A complete, free and open-source evolutionary framework written in Python",
   license = "PSF",
   keywords = "genetic algorithm genetic programming algorithms framework library python ai evolutionary framework",
   url = "http://pyevolve.sourceforge.net/",
)
