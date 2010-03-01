"""

:mod:`Mutators` -- mutation methods module
=====================================================================

In this module we have the genetic operators of mutation for each chromosome representation.

"""

import Util
from random import randint as rand_randint, gauss as rand_gauss, uniform as rand_uniform
import Consts

#############################
##     1D Binary String    ##
#############################

def G1DBinaryStringMutatorSwap(genome, **args):
   """ The 1D Binary String Swap Mutator """

   if args["pmut"] <= 0.0: return 0
   stringLength = len(genome)
   mutations = args["pmut"] * (stringLength)
   
   if mutations < 1.0:
      mutations = 0
      for it in xrange(stringLength):
         if Util.randomFlipCoin(args["pmut"]):
            Util.listSwapElement(genome, it, rand_randint(0, stringLength-1))
            mutations+=1

   else:
      for it in xrange(int(round(mutations))):
         Util.listSwapElement(genome, rand_randint(0, stringLength-1),
                                      rand_randint(0, stringLength-1))

   return mutations

def G1DBinaryStringMutatorFlip(genome, **args):
   """ The classical flip mutator for binary strings """
   if args["pmut"] <= 0.0: return 0
   stringLength = len(genome)
   mutations = args["pmut"] * (stringLength)
   
   if mutations < 1.0:
      mutations = 0
      for it in xrange(stringLength):
         if Util.randomFlipCoin(args["pmut"]):
            if genome[it] == 0: genome[it] = 1
            else: genome[it] = 0
            mutations+=1

   else:
      for it in xrange(int(round(mutations))):
         which = rand_randint(0, stringLength-1)
         if genome[which] == 0: genome[which] = 1
         else: genome[which] = 0

   return mutations

####################
##     1D List    ##
####################

def G1DListMutatorSwap(genome, **args):
   """ The mutator of G1DList, Swap Mutator """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome) - 1
   mutations = args["pmut"] * (listSize+1)

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize+1):
         if Util.randomFlipCoin(args["pmut"]):
            Util.listSwapElement(genome, it, rand_randint(0, listSize))
            mutations+=1
   else:
      for it in xrange(int(round(mutations))):
         Util.listSwapElement(genome, rand_randint(0, listSize), rand_randint(0, listSize))

   return mutations

def G1DListMutatorIntegerRange(genome, **args):
   """ Simple integer range mutator for G1DList

   Accepts the *rangemin* and *rangemax* genome parameters, both optional.

   """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome)
   mutations = args["pmut"] * (listSize)

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize):
         if Util.randomFlipCoin(args["pmut"]):
            genome[it] = rand_randint(genome.getParam("rangemin", Consts.CDefRangeMin),
                         genome.getParam("rangemax", Consts.CDefRangeMax))
            mutations += 1
   
   else: 
      for it in xrange(int(round(mutations))):
         which_gene = rand_randint(0, listSize-1)
         genome[which_gene] = rand_randint(genome.getParam("rangemin", Consts.CDefRangeMin),
                              genome.getParam("rangemax", Consts.CDefRangeMax))

   return mutations


def G1DListMutatorRealRange(genome, **args):
   """ Simple real range mutator for G1DList

   Accepts the *rangemin* and *rangemax* genome parameters, both optional.

   """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome)
   mutations = args["pmut"] * (listSize)

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize):
         if Util.randomFlipCoin(args["pmut"]):
            genome[it] = rand_uniform(genome.getParam("rangemin", Consts.CDefRangeMin),
                         genome.getParam("rangemax", Consts.CDefRangeMax))
            mutations += 1
   
   else: 
      for it in xrange(int(round(mutations))):
         which_gene = rand_randint(0, listSize-1)
         genome[which_gene] = rand_uniform(genome.getParam("rangemin", Consts.CDefRangeMin),
                              genome.getParam("rangemax", Consts.CDefRangeMax))

   return mutations

def G1DListMutatorIntegerGaussian(genome, **args):
   """ A gaussian mutator for G1DList of Integers

   Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
   accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
   represents the mean and the std. dev. of the random distribution.

   """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome)
   mutations = args["pmut"] * (listSize)
   
   mu = genome.getParam("gauss_mu")
   sigma = genome.getParam("gauss_sigma")

   if mu is None:
      mu = Consts.CDefG1DListMutIntMU
   
   if sigma is None:
      sigma = Consts.CDefG1DListMutIntSIGMA

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize):
         if Util.randomFlipCoin(args["pmut"]):
            final_value = genome[it] + int(rand_gauss(mu, sigma))

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome[it] = final_value
            mutations += 1
   else: 
      for it in xrange(int(round(mutations))):
         which_gene = rand_randint(0, listSize-1)
         final_value = genome[which_gene] + int(rand_gauss(mu, sigma))

         final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
         final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

         genome[which_gene] = final_value

   return mutations


def G1DListMutatorRealGaussian(genome, **args):
   """ The mutator of G1DList, Gaussian Mutator

   Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
   accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
   represents the mean and the std. dev. of the random distribution.

   """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome)
   mutations = args["pmut"] * (listSize)

   mu = genome.getParam("gauss_mu")
   sigma = genome.getParam("gauss_sigma")

   if mu is None:
      mu = Consts.CDefG1DListMutRealMU
   
   if sigma is None:
      sigma = Consts.CDefG1DListMutRealSIGMA

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize):
         if Util.randomFlipCoin(args["pmut"]):
            final_value = genome[it] + rand_gauss(mu, sigma)

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome[it] = final_value
            mutations += 1
   else:
      for it in xrange(int(round(mutations))):
         which_gene = rand_randint(0, listSize-1)
         final_value = genome[which_gene] + rand_gauss(0, 1)

         final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
         final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

         genome[which_gene] = final_value

   return mutations

def G1DListMutatorIntegerBinary(genome, **args):
   """ The mutator of G1DList, the binary mutator

   This mutator will random change the 0 and 1 elements of the 1D List.

   """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome)
   mutations = args["pmut"] * (listSize)

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize):
         if Util.randomFlipCoin(args["pmut"]):
            if genome[it] == 0: genome[it] = 1
            elif genome[it] == 1: genome[it] = 0

            mutations += 1
   else:
      for it in xrange(int(round(mutations))):
         which_gene = rand_randint(0, listSize-1)
         if genome[which_gene] == 0: genome[which_gene] = 1
         elif genome[which_gene] == 1: genome[which_gene] = 0

   return mutations

def G1DListMutatorAllele(genome, **args):
   """ The mutator of G1DList, Allele Mutator

   To use this mutator, you must specify the *allele* genome parameter with the
   :class:`GAllele.GAlleles` instance.

   """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome) - 1
   mutations = args["pmut"] * (listSize+1)

   allele = genome.getParam("allele", None)
   if allele is None:
      Util.raiseException("to use the G1DListMutatorAllele, you must specify the 'allele' parameter", TypeError)

   if mutations < 1.0:
      mutations = 0
      for it in xrange(listSize+1):
         if Util.randomFlipCoin(args["pmut"]):
            new_val = allele[it].getRandomAllele()
            genome[it] = new_val
            mutations+=1
   else:
      for it in xrange(int(round(mutations))):
         which_gene = rand_randint(0, listSize)
         new_val = allele[which_gene].getRandomAllele()
         genome[which_gene] = new_val

   return mutations


####################
##     2D List    ##
####################

def G2DListMutatorSwap(genome, **args):
   """ The mutator of G1DList, Swap Mutator """
   
   if args["pmut"] <= 0.0: return 0
   height, width = genome.getSize()
   elements = height * width

   mutations = args["pmut"] * elements

   if mutations < 1.0:
      mutations = 0
      for i in xrange(height):
         for j in xrange(width):
            if Util.randomFlipCoin(args["pmut"]):
               index_b = (rand_randint(0, height-1), rand_randint(0, width-1))
               Util.list2DSwapElement(genome.genomeList, (i,j), index_b)
               mutations+=1
   else:
      for it in xrange(int(round(mutations))):
         index_a = (rand_randint(0, height-1), rand_randint(0, width-1))
         index_b = (rand_randint(0, height-1), rand_randint(0, width-1))
         Util.list2DSwapElement(genome.genomeList, index_a, index_b)

   return mutations


def G2DListMutatorIntegerGaussian(genome, **args):
   """ A gaussian mutator for G2DList of Integers 

   Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
   accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
   represents the mean and the std. dev. of the random distribution.

   """
   if args["pmut"] <= 0.0: return 0
   height, width = genome.getSize()
   elements = height * width

   mutations = args["pmut"] * elements

   mu = genome.getParam("gauss_mu")
   sigma = genome.getParam("gauss_sigma")

   if mu is None:
      mu = Consts.CDefG2DListMutIntMU
   
   if sigma is None:
      sigma = Consts.CDefG2DListMutIntSIGMA

   if mutations < 1.0:
      mutations = 0
      
      for i in xrange(genome.getHeight()):
         for j in xrange(genome.getWidth()):
            if Util.randomFlipCoin(args["pmut"]):
               final_value = genome[i][j] + int(rand_gauss(mu, sigma))

               final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
               final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

               genome.setItem(i, j, final_value)
               mutations += 1
   else: 

      for it in xrange(int(round(mutations))):
         which_x = rand_randint(0, genome.getWidth()-1)
         which_y = rand_randint(0, genome.getHeight()-1)

         final_value = genome[which_y][which_x] + int(rand_gauss(mu, sigma))

         final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
         final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

         genome.setItem(which_y, which_x, final_value)

   return mutations


def G2DListMutatorAllele(genome, **args):
   """ The mutator of G2DList, Allele Mutator

   To use this mutator, you must specify the *allele* genome parameter with the
   :class:`GAllele.GAlleles` instance.

   .. warning:: the :class:`GAllele.GAlleles` instance must have the homogeneous flag enabled

   """
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome) - 1
   mutations = args["pmut"] * (listSize+1)

   allele = genome.getParam("allele", None)
   if allele is None:
      Util.raiseException("to use the G2DListMutatorAllele, you must specify the 'allele' parameter", TypeError)

   if allele.homogeneous == False:
      Util.raiseException("to use the G2DListMutatorAllele, the 'allele' must be homogeneous")

   if mutations < 1.0:
      mutations = 0

      for i in xrange(genome.getHeight()):
         for j in xrange(genome.getWidht()):
            if Util.randomFlipCoin(args["pmut"]):
               new_val = allele[0].getRandomAllele()
               genome.setItem(i, j, new_val)
               mutations+=1
   else:
      for it in xrange(int(round(mutations))):
         which_x = rand_randint(0, genome.getWidth()-1)
         which_y = rand_randint(0, genome.getHeight()-1)

         new_val = allele[0].getRandomAllele()
         genome.setItem(which_x, which_y, new_val)

   return mutations


def G2DListMutatorRealGaussian(genome, **args):
   """ A gaussian mutator for G2DList of Real 

   Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
   accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
   represents the mean and the std. dev. of the random distribution.

   """
   if args["pmut"] <= 0.0: return 0
   height, width = genome.getSize()
   elements = height * width

   mutations = args["pmut"] * elements

   mu = genome.getParam("gauss_mu")
   sigma = genome.getParam("gauss_sigma")

   if mu is None:
      mu = Consts.CDefG2DListMutRealMU
   
   if sigma is None:
      sigma = Consts.CDefG2DListMutRealSIGMA

   if mutations < 1.0:
      mutations = 0
      
      for i in xrange(genome.getHeight()):
         for j in xrange(genome.getWidth()):
            if Util.randomFlipCoin(args["pmut"]):
               final_value = genome[i][j] + rand_gauss(mu, sigma)

               final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
               final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

               genome.setItem(i, j, final_value)
               mutations += 1
   else: 

      for it in xrange(int(round(mutations))):
         which_x = rand_randint(0, genome.getWidth()-1)
         which_y = rand_randint(0, genome.getHeight()-1)

         final_value = genome[which_y][which_x] + rand_gauss(mu, sigma)

         final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
         final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

         genome.setItem(which_y, which_x, final_value)

   return mutations
