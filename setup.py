from distutils.core import setup #changed to distutils.core for pypy comptibility
from pyevolve import __version__, __author__

setup(
   name = "Pyevolve",
   version = __version__,
   packages = ["pyevolve"],
   scripts = ['pyevolve_graph.py'],
   package_data = {
      'pyevolve': ['*.txt']
   },
   author = __author__,
   author_email = "christian.perone@gmail.com",
   description = "A complete, free and open-source evolutionary framework written in Python",
   license = "PSF",
   keywords = "genetic algorithm genetic programming algorithms framework library python ai evolutionary framework",
   url = "http://pyevolve.sourceforge.net/"
)
