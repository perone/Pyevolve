"""

:mod:`Statistics` -- statistical structure module
==========================================================================

This module have the class which is reponsible to keep statistics of each
generation. This class is used by the adapters and other statistics dump objects.

"""
class Statistics:
   """ Statistics Class - A class bean-like to store the statistics

   The statistics hold by this class are:

   **rawMax, rawMin, rawAve**
      Maximum, minimum and average of raw scores

   **rawDev, rawVar**
      Standard Deviation and Variance of raw scores

   **fitMax, fitMin, fitAve**
      Maximum, mininum and average of fitness scores

   **rawTot, fitTot**
      The total (sum) of raw scores and the fitness scores

   Example:
      >>> stats = ga_engine.getStatistics()
      >>> st["rawMax"]
      10.2
   """

   def __init__(self):
      """ The Statistics Class creator """

      # 'fit' means 'fitness'
      self.internalDict = {   "rawMax"  : 0.0,
                              "rawMin"  : 0.0,
                              "rawAve"  : 0.0,
                              "rawDev"  : 0.0,
                              "rawVar"  : 0.0,
                              "fitMax"  : 0.0,
                              "fitMin"  : 0.0,
                              "fitAve"  : 0.0 }

      self.descriptions = {   "rawMax" : "Maximum raw score",
                              "rawMin" : "Minimum raw score",
                              "rawAve" : "Average of raw scores",
                              "rawDev" : "Standard deviation of raw scores",
                              "rawVar" : "Raw scores variance",
                              "fitMax" : "Maximum fitness",
                              "fitMin" : "Minimum fitness",
                              "fitAve" : "Fitness average" }
   def __getitem__(self, key):
      """ Return the specific statistic by key """
      return self.internalDict[key]

   def __setitem__(self, key, value):
      """ Set the statistic """
      self.internalDict[key] = value

   def __len__(self):
      """ Return the lenght of internal stats dictionary """
      return len(self.internalDict)

   def __repr__(self):
      """ Return a string representation of the statistics """
      strBuff  = "- Statistics\n"
      for k,v in self.internalDict.items():
         strBuff += "\t%-45s = %.2f\n" % (self.descriptions.get(k, k), v)
      return strBuff

   def asTuple(self):
      """ Returns the stats as a python tuple """
      return tuple(self.internalDict.values())

   def clear(self):
      """ Set all statistics to zero """
      for k in self.internalDict.keys():
         self.internalDict[k] = 0

   def items(self):
      """ Return a tuple (name, value) for all stored statistics """
      return self.internalDict.items()

   def clone(self):
      """ Instantiate a new Statistic class with the same contents """
      clone_stat = Statistics()
      self.copy(clone_stat)
      return clone_stat
   
   def copy(self, obj):
      """ Copy the values to the obj variable of the same class
      
      :param obj: the Statistics object destination

      """
      obj.internalDict = self.internalDict.copy()
      obj.descriptions = self.descriptions.copy()
      

      