"""
:mod:`GPopulation` -- the population module
================================================================

This module contains the :class:`GPopulation.GPopulation` class, which is reponsible
to keep the population and the statistics.

"""

import Consts
from FunctionSlot import FunctionSlot
from Statistics import Statistics
from math import sqrt as math_sqrt
import logging

def key_raw_score(individual):
   """ A key function to return raw score

   :param individual: the individual instance
   :rtype: the individual raw score

   .. note:: this function is used by the max()/min() python functions

   """
   return individual.score

def key_fitness_score(individual):
   """ A key function to return fitness score, used by max()/min()

   :param individual: the individual instance
   :rtype: the individual fitness score

   .. note:: this function is used by the max()/min() python functions

   """
   return individual.fitness

def cmp_individual_raw(a, b):
   """ Compares two individual raw scores

   Example:
      >>> GPopulation.cmp_individual_raw(a, b)
   
   :param a: the A individual instance
   :param b: the B individual instance
   :rtype: 0 if the two individuals raw score are the same,
           -1 if the B individual raw score is greater than A and
           1 if the A individual raw score is greater than B.

   .. note:: this function is used to sorte the population individuals

   """
   if a.score < b.score: return -1
   if a.score > b.score: return 1
   return 0
   
def cmp_individual_scaled(a, b):
   """ Compares two individual fitness scores, used for sorting population

   Example:
      >>> GPopulation.cmp_individual_scaled(a, b)
   
   :param a: the A individual instance
   :param b: the B individual instance
   :rtype: 0 if the two individuals fitness score are the same,
           -1 if the B individual fitness score is greater than A and
           1 if the A individual fitness score is greater than B.

   .. note:: this function is used to sorte the population individuals

   """
   if a.fitness < b.fitness: return -1
   if a.fitness > b.fitness: return 1
   return 0

class GPopulation:
   """ GPopulation Class - The container for the population

   **Examples**
      Get the population from the :class:`GSimpleGA.GSimpleGA` (GA Engine) instance
         >>> pop = ga_engine.getPopulation()

      Get the best fitness individual
         >>> bestIndividual = pop.bestFitness()

      Get the best raw individual
         >>> bestIndividual = pop.bestRaw()

      Get the statistics from the :class:`Statistics.Statistics` instance
         >>> stats = pop.getStatistics()
         >>> print stats["rawMax"]
         10.4

      Iterate, get/set individuals
         >>> for ind in pop:
         >>>   print ind
         (...)
         
         >>> for i in xrange(len(pop)):
         >>>    print pop[i]
         (...)

         >>> pop[10] = newGenome
         >>> pop[10].fitness
         12.5

   :param genome: the :term:`Sample genome`

   """

   def __init__(self, genome):
      """ The GPopulation Class creator """

      logging.debug("New population instance, %s class genomes.", genome.__class__.__name__)
      self.oneSelfGenome = genome
      self.internalPop   = []
      self.popSize       = 0
      self.sortType      = Consts.CDefPopSortType
      self.sorted        = False
      self.minimax       = Consts.CDefPopMinimax
      self.scaleMethod   = FunctionSlot("Scale Method")
      self.scaleMethod.set(Consts.CDefPopScale)
      self.allSlots      = [self.scaleMethod]

      # Statistics
      self.statted = False
      self.stats   = Statistics()

   def setMinimax(minimax):
      """ Sets the population minimax

      Example:
         >>> pop.setMinimax(Consts.minimaxType["maximize"])
   
      :param minimax: the minimax type

      """
      self.minimax = minimax

   def __repr__(self):
      """ Returns the string representation of the population """
      ret =  "- GPopulation\n"
      ret += "\tPopulation Size:\t %d\n" % (self.popSize,)
      ret += "\tSort Type:\t\t %s\n" % (Consts.sortType.keys()[Consts.sortType.values().index(self.sortType)].capitalize(),)
      ret += "\tMinimax Type:\t\t %s\n" % (Consts.minimaxType.keys()[Consts.minimaxType.values().index(self.minimax)].capitalize(),)
      for slot in self.allSlots:
         ret+= "\t" + slot.__repr__()
      ret+="\n"
      ret+= self.stats.__repr__()
      return ret

   def __len__(self):
      """ Return the length of population """
      return len(self.internalPop)
      
   def __getitem__(self, key):
      """ Returns the specified individual from population """
      return self.internalPop[key]

   def __iter__(self):
      """ Returns the iterator of the population """
      return iter(self.internalPop)

   def __setitem__(self, key, value):
      """ Set an individual of population """
      self.internalPop[key] = value
      self.__clear_flags()

   def __clear_flags(self):
      self.sorted = False
      self.statted = False

   def getStatistics(self):
      """ Return a Statistics class for statistics

      :rtype: the :class:`Statistics.Statistics` instance

      """
      self.statistics()
      return self.stats      

   def statistics(self):
      """ Do statistical analysis of population and set 'statted' to True """
      if self.statted: return
      logging.debug("Running statistical calc.")
      raw_sum = 0

      len_pop = len(self)
      for ind in xrange(len_pop):
         raw_sum += self[ind].score

      self.stats["rawMax"] = max(self, key=key_raw_score).score
      self.stats["rawMin"] = min(self, key=key_raw_score).score
      self.stats["rawAve"] = raw_sum / float(len_pop)
      
      tmpvar = 0.0;
      for ind in xrange(len_pop):
         s = self[ind].score - self.stats["rawAve"]
         s*= s
         tmpvar += s

      tmpvar/= float((len(self) - 1))
      self.stats["rawDev"] = math_sqrt(tmpvar)
      self.stats["rawVar"] = tmpvar

      self.statted = True

   def bestFitness(self, index=0):
      """ Return the best scaled fitness individual of population

      :param index: the *index* best individual
      :rtype: the individual

      """
      self.sort()
      return self.internalPop[index]

   def bestRaw(self):
      """ Return the best raw score individual of population

      :rtype: the individual
      
      """
      if self.minimax == Consts.minimaxType["minimize"]:
         return min(self, key=key_raw_score)
      else:
         return max(self, key=key_raw_score)

   def sort(self):
      """ Sort the population """
      if self.sorted: return
      rev = (self.minimax == Consts.minimaxType["maximize"])

      if self.sortType == Consts.sortType["raw"]:
         self.internalPop.sort(cmp=cmp_individual_raw, reverse=rev)
      else:
         self.scale()
         self.internalPop.sort(cmp=cmp_individual_scaled, reverse=rev)

      self.sorted = True

   def setPopulationSize(self, size):
      """ Set the population size

      :param size: the population size

      """
      self.popSize = size

   def setSortType(self, sort_type):
      """ Sets the sort type

      Example:
         >>> pop.setSortType(Consts.sortType["scaled"])

      :param sort_type: the Sort Type

      """
      self.sortType = sort_type

   def create(self, **args):
      """ Clone the example genome to fill the population """
      self.clear()
      self.minimax = args["minimax"]
      for i in xrange(self.popSize):
         self.internalPop.append(self.oneSelfGenome.clone())
      self.__clear_flags()

   def initialize(self):
      """ Initialize all individuals of population,
      this calls the initialize() of individuals """
      for gen in self.internalPop:
         gen.initialize()
      self.__clear_flags()

   def evaluate(self, **args):
      """ Evaluate all individuals in population, calls the evaluate() method of individuals
   
      :param args: this params are passed to the evaluation function

      """
      for ind in self.internalPop:
         ind.evaluate(**args)
      self.__clear_flags()

   def scale(self, **args):
      """ Scale the population using the scaling method

      :param args: this parameter is passed to the scale method

      """
      for it in self.scaleMethod.applyFunctions(self, **args):
         pass

      fit_sum = 0
      for ind in xrange(len(self)):
         fit_sum += self[ind].fitness

      self.stats["fitMax"] = max(self, key=key_fitness_score).fitness
      self.stats["fitMin"] = min(self, key=key_fitness_score).fitness
      self.stats["fitAve"] = fit_sum / float(len(self))

      self.sorted = False

   def printStats(self):
      """ Print statistics of the current population """
      message = ""
      if self.sortType == Consts.sortType["scaled"]:
         message =  "Max/Min/Avg Fitness(Raw) [%.2f(%.2f)/%.2f(%.2f)/%.2f(%.2f)]" % (self.stats["fitMax"], self.stats["rawMax"], self.stats["fitMin"], self.stats["rawMin"], self.stats["fitAve"], self.stats["rawAve"])
      else:
         message = "Max/Min/Avg Raw [%.2f/%.2f/%.2f]" % (self.stats["rawMax"], self.stats["rawMin"], self.stats["rawAve"])
      logging.info(message)
      print message
      return message

   def copy(self, pop):
      """ Copy current population to 'pop'

      :param pop: the destination population

      .. warning:: this method do not copy the individuals, only the population logic

      """
      pop.popSize = self.popSize
      pop.sortType = self.sortType
      pop.sorted = self.sorted
      pop.statted = self.statted
      pop.minimax = self.minimax
      pop.scaleMethod = self.scaleMethod
   
   def clear(self):
      """ Remove all individuals from population """
      del self.internalPop[:]
      self.__clear_flags()
      
   def clone(self):
      """ Return a brand-new cloned population """
      newpop = GPopulation(self.oneSelfGenome.clone())
      self.copy(newpop)
      return newpop
      

