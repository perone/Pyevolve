"""

:mod:`GAllele` -- the genome alleles module
===========================================================

In this module, there are the :class:`GAllele.GAlleles` class (which is the
class that holds the allele types) and all the
allele types to use with the supported chromosomes.

"""
import random
import Consts
import Util

class GAlleles:
   """ GAlleles Class - The set of alleles

   Example:
      >>> alleles = GAlleles()
      >>> choices = [1,2,3,4]
      >>> lst = GAlleleList(choices)
      >>> alleles.add(lst)
      >>> alleles[0].getRandomAllele() in lst
      True

   :param allele_list: the list of alleles
   :param homogeneous: if is True, all the alleles will be use only the first added

   """

   def __init__(self, allele_list = [], homogeneous=False):
      """ The constructor of GAlleles class """
      self.allele_list = []
      self.allele_list.extend(allele_list)
      self.homogeneous = homogeneous
     
   def add(self, allele):
      """ Appends one allele to the alleles list
      
      :param allele: allele to be added

      """
      self.allele_list.append(allele)

   def __getslice__(self, a, b):
      """ Returns the slice part of alleles list """
      return self.allele_list[a:b]

   def __getitem__(self, index):
      """ Returns the index allele of the alleles list """
      if self.homogeneous: return self.allele_list[0]
      try:
         val = self.allele_list[index]
      except IndexError:
         Util.raiseException(
         """An error was occurred while finding allele for the %d position of chromosome.
           You may consider use the 'homogeneous' parameter of the GAlleles class.
         """ % (index,))
      return val

   def __setitem__(self, index, value):
      """ Sets the index allele of the alleles list """
      if self.homogeneous: self.allele_list[0] = value
      self.allele_list[index] = value

   def __iter__(self):
      """ Return the list iterator """
      if self.homogeneous:
         oneList = [self.allele_list[0]]
         return iter(oneList)
      return iter(self.allele_list)

   def __len__(self):
      """ Returns the lenght of the alleles list """
      if self.homogeneous: return 1
      return len(self.allele_list)

   def __repr__(self):
      """ Return a string representation of the allele """
      ret = "- GAlleles\n"
      ret += "\tHomogeneous:\t %s\n" % (self.homogeneous,)
      ret += "\tList size:\t %s\n" % (len(self),)
      ret += "\tAlleles:\n\n"
      if self.homogeneous:
         ret += "Allele for 0 position:\n"
         ret += self.allele_list[0].__repr__()
      else:
         for i in xrange(len(self)):
            ret += "Allele for %d position:\n" % (i,)
            ret += self.allele_list[i].__repr__()
      return ret


class GAlleleList:
   """ GAlleleList Class - The list allele type

   Example:
      >>> alleles = GAlleles()
      >>> choices = [1,2,3,4]
      >>> lst = GAlleleList(choices)
      >>> alleles.add(lst)
      >>> alleles[0].getRandomAllele() in lst
      True

   """

   def __init__(self, options=[]):
      """ The constructor of GAlleleList class """
      self.options = []
      self.options.extend(options)

   def clear(self):
      """ Removes all the allele options from the list """
      del self.options[:]
   
   def getRandomAllele(self):
      """ Returns one random choice from the options list """
      return random.choice(self.options)

   def add(self, option):
      """ Appends one option to the options list

      :param option: option to be added in the list         

      """
      self.options.append(option)

   def __getslice__(self, a, b):
      """ Returns the slice part of options """
      return self.options[a:b]

   def __getitem__(self, index):
      """ Returns the index option from the options list """
      return self.options[index]

   def __setitem__(self, index, value):
      """ Sets the index option of the list """
      self.options[index] = value

   def __iter__(self):
      """ Return the list iterator """
      return iter(self.options)

   def __len__(self):
      """ Returns the lenght of the options list """
      return len(self.options)

   def remove(self, option):
      """ Removes the option from list

      :param option: remove the option from the list

      """
      self.options.remove(option)

   def __repr__(self):
      """ Return a string representation of the allele """
      ret = "- GAlleleList\n"
      ret += "\tList size:\t %s\n" % (len(self),)
      ret += "\tAllele Options:\t %s\n\n" % (self.options,) 
      return ret

class GAlleleRange:
   """ GAlleleRange Class - The range allele type

   Example:
      >>> ranges = GAlleleRange(0,100)
      >>> ranges.getRandomAllele() >= 0 and ranges.getRandomAllele() <= 100
      True

   :param begin: the begin of the range
   :param end: the end of the range
   :param real: if True, the range will be of real values

   """

   def __init__(self, begin=Consts.CDefRangeMin,
                end=Consts.CDefRangeMax, real=False):
      """ The constructor of GAlleleRange class """
      self.beginEnd = [(begin, end)]
      self.real = real

   def add(self, begin, end):
      """ Add a new range

      :param begin: the begin of range
      :param end: the end of the range

      """
      self.beginEnd.append((begin, end))

   def clear(self):
      """ Removes all ranges """
      del self.beginEnd[:]

   def getRandomAllele(self):
      """ Returns one random choice between the range """
      rand_func = random.uniform if self.real else random.randint

      choice = random.randint(0, len(self.beginEnd)-1)
      return rand_func(self.beginEnd[choice][0], self.beginEnd[choice][1])

   def setReal(self, flag=True):
      """ Sets True if the range is real or False if is integer

      :param flag: True or False

      """
      self.real = flag

   def getReal(self):
      """ Returns True if the range is real or False if it is integer """
      return self.real

   def __len__(self):
      """ Returns the ranges in the allele """
      return len(self.beginEnd)

   def __repr__(self):
      """ Return a string representation of the allele """
      ret = "- GAlleleRange\n"
      ret += "\tReal:\t\t %s\n" % (self.real,)
      ret += "\tRanges Count:\t %s\n" % (len(self),)
      ret += "\tRange List:\n"
      for beg, end in self.beginEnd:
         ret += "\t\t\t Range from [%s] to [%s]\n" % (beg, end)
      ret += "\n"
      return ret

