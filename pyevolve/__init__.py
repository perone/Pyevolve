"""
:mod:`pyevolve` -- the main pyevolve namespace
================================================================

This is the main module of the pyevolve, every other module
is above this namespace, for example, to import :mod:`Mutators`:

   >>> from pyevolve import Mutators


"""
__all__ = ["Consts", "Crossovers", "DBAdapters", "FunctionSlot",
           "G1DBinaryString", "G1DList", "G2DBinaryString",
           "G2DList", "GAllele", "GenomeBase", "GPopulation",
           "GSimpleGA", "GTree", "Initializators",
           "Migration", "Mutators", "Network", "Scaling", "Selectors",
           "Statistics", "Util"]

__version__ =  '0.6rc1'
__author__ =  'Christian S. Perone'

import pyevolve.Consts
import sys

if sys.version_info[:2] < Consts.CDefPythonRequire:
   raise Exception("Python 2.5+ required, the version %s was found on your system !" % (sys.version_info[:2],))

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
                    filemode='w')   logging.info("Pyevolve v.%s, the log was enabled by user.", __version__)
