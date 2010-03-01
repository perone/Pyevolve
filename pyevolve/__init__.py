"""
:mod:`pyevolve` -- the main pyevolve namespace
================================================================

This is the main module of the pyevolve, every other module
is above this namespace, for example, to import :mod:`Mutators`:

   >>> from pyevolve import Mutators


"""
__version__=  '0.5'
__author__ =  'Christian S. Perone'

import Consts
import sys

if sys.version_info < Consts.CDefPythonRequire:
   import logging
   raise Exception("Python 2.5+ required !")
else:
   del sys

def logEnable(filename=Consts.CDefLogFile, level=Consts.CDefLogLevel):
   """ Enable the log system for pyevolve

   :param filename: the log filename
   :param level: the debugging level

   Example:
      >>> pyevolve.logEnable()

   """
   import logging
   logging.basicConfig(level=level,
                    format='%(asctime)s [%(module)s:%(funcName)s:%(lineno)d] %(levelname)s %(message)s',
                    filename=filename,
                    filemode='w')
