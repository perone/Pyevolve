from setuptools import setup, find_packages
from pyevolve import __version__, __author__

setup(
   name = "Pyevolve",
   version = __version__,
   packages = find_packages(),
   scripts = ['pyevolve_graph.py'],
   package_data = {
      'pyevolve': ['*.txt']
   },
   author = __author__,
   author_email = "christian.perone@gmail.com",
   description = "A complete python genetic algorithm framework",
   license = "PSF",
   keywords = "genetic algorithm algorithms framework library python",
   url = "http://pyevolve.sourceforge.net/", 
   download_url = "https://sourceforge.net/project/showfiles.php?group_id=251160"
)
