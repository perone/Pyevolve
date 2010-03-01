"""

:mod:`GSimpleGA` -- the genetic algorithm by itself
=====================================================================

This module contains the GA Engine, the GA Engine class is responsible
for all the evolutionary process. It contains the GA Engine related
funtions, like the Termination Criteria functions for convergence analysis, etc.

"""

from GPopulation import GPopulation
from FunctionSlot import FunctionSlot
import Consts
import Util
import random
import logging
from time import time
from types import BooleanType
from sys import exit as sys_exit
from sys import platform as sys_platform

import code
import pyevolve

if sys_platform[:3] == "win":
   import msvcrt
elif sys_platform[:5] == "linux":
   import atexit
   atexit.register(Util.set_normal_term)
   Util.set_curses_term()

def RawScoreCriteria(ga_engine):
   """ Terminate the evolution using the bestRawScore parameter obtained from the individual

   Example:
      >>> genome.setParams(bestRawScore=0.00, roundDecimal=2)
      (...)
      >>> ga_engine.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

   """
   ind = ga_engine.bestIndividual()
   bestRawScore = ind.getParam("bestRawScore")
   roundDecimal = ind.getParam("roundDecimal")

   if bestRawScore is None:
      Util.raiseException("you must specify the bestRawScore parameter", ValueError)

   if ga_engine.getMinimax() == Consts.minimaxType["maximize"]:
      if roundDecimal is not None:
         return round(bestRawScore, roundDecimal) <= round(ind.score, roundDecimal)
      else:
         return bestRawScore <= ind.score
   else:
      if roundDecimal is not None:
         return round(bestRawScore, roundDecimal) >= round(ind.score, roundDecimal)
      else:
         return bestRawScore >= ind.score

   return flag

def ConvergenceCriteria(ga_engine):
   """ Terminate the evolution when the population have converged

   Example:
      >>> ga_engine.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

   """
   pop = ga_engine.getPopulation()
   return pop[0] == pop[len(pop)-1]
   
def RawStatsCriteria(ga_engine):
   """ Terminate the evolution based on the raw stats

   Example:
      >>> ga_engine.terminationCriteria.set(GSimpleGA.RawStatsCriteria)

   """
   stats = ga_engine.getStatistics()
   if stats["rawMax"] == stats["rawMin"]:
      if stats["rawAve"] == stats["rawMax"]:
         return True
   return False

def FitnessStatsCriteria(ga_engine):
   """ Terminate the evoltion based on the fitness stats

   Example:
      >>> ga_engine.terminationCriteria.set(GSimpleGA.FitnessStatsCriteria)


   """
   stats = ga_engine.getStatistics()
   if stats["fitMax"] == stats["fitMin"]:
      if stats["fitAve"] == stats["fitMax"]:
         return True
   return False

class GSimpleGA:
   """ GA Engine Class - The Genetic Algorithm Core

   Example:
      >>> ga = GSimpleGA.GSimpleGA(genome)
      >>> ga.selector.set(Selectors.GRouletteWheel)
      >>> ga.setGenerations(120)
      >>> ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

   :param genome: the :term:`Sample Genome`
   :param interactiveMode: this flag enables the Interactive Mode, the default is True
   :param seed: the random seed value

   .. note:: if you use the same ramdom seed, all the runs of algorithm will be the same

   """

   selector = None
   """ This is the function slot for the selection method
   if you want to change the default selector, you must do this: ::

      ga_engine.selector.set(Selectors.GRouletteWheel) """

   stepCallback = None
   """ This is the :term:`step callback function` slot,
   if you want to set the function, you must do this: ::
      
      def your_func(ga_engine):
         # Here you have access to the GA Engine
         return False

      ga_engine.stepCallback.set(your_func)
      
   now *"your_func"* will be called every generation.
   When this function returns True, the GA Engine will stop the evolution and show
   a warning, if is False, the evolution continues.
   """

   terminationCriteria = None
   """ This is the termination criteria slot, if you want to set one
   termination criteria, you must do this: ::

      ga_engine.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
      
   Now, when you run your GA, it will stop when the population converges.

   There are those termination criteria functions: :func:`GSimpleGA.RawScoreCriteria`, :func:`GSimpleGA.ConvergenceCriteria`, :func:`GSimpleGA.RawStatsCriteria`, :func:`GSimpleGA.FitnessStatsCriteria`

   But you can create your own termination function, this function receives
   one parameter which is the GA Engine, follows an example: ::

      def ConvergenceCriteria(ga_engine):
         pop = ga_engine.getPopulation()
         return pop[0] == pop[len(pop)-1]

   When this function returns True, the GA Engine will stop the evolution and show
   a warning, if is False, the evolution continues, this function is called every
   generation.
   """

   def __init__(self, genome, seed=None, interactiveMode=True):
      """ Initializator of GSimpleGA """
      random.seed(seed)
      self.internalPop  = GPopulation(genome)
      self.nGenerations = Consts.CDefGAGenerations
      self.pMutation    = Consts.CDefGAMutationRate
      self.pCrossover   = Consts.CDefGACrossoverRate
      self.setPopulationSize(Consts.CDefGAPopulationSize)
      self.minimax      = Consts.minimaxType["maximize"]
      self.elitism      = True
      self.dbAdapter    = None
      self.time_init    = None
      self.interactiveMode = interactiveMode

      self.selector = FunctionSlot("Selector")
      self.stepCallback = FunctionSlot("Generation Step Callback")
      self.terminationCriteria = FunctionSlot("Termination Criteria")
      self.selector.set(Consts.CDefGASelector)
      self.allSlots = [ self.selector, self.stepCallback, self.terminationCriteria ]
      
      self.currentGeneration = 0
      
      logging.debug("A GA Engine was created, nGenerations=%d", self.nGenerations)

   def __repr__(self):
      """ The string representation of the GA Engine """
      ret =  "- GSimpleGA\n"
      ret += "\tPopulation Size:\t %d\n" % (self.internalPop.popSize,)
      ret += "\tGenerations:\t\t %d\n" % (self.nGenerations,)
      ret += "\tCurrent Generation:\t %d\n" % (self.currentGeneration,)
      ret += "\tMutation Rate:\t\t %.2f\n" % (self.pMutation,)
      ret += "\tCrossover Rate:\t\t %.2f\n" % (self.pCrossover,)
      ret += "\tMinimax Type:\t\t %s\n" % (Consts.minimaxType.keys()[Consts.minimaxType.values().index(self.minimax)].capitalize(),)
      ret += "\tElitism:\t\t %s\n" % (self.elitism,)
      ret += "\tDB Adapter:\t\t %s\n" % (self.dbAdapter,)
      for slot in self.allSlots:
         ret+= "\t" + slot.__repr__()
      ret+="\n"
      return ret
   
   def setDBAdapter(self, dbadapter):
      """ Sets the DB Adapter of the GA Engine
      
      :param dbadapter: one of the :mod:`DBAdapters` classes instance

      .. warning:: the use the of a DB Adapter can reduce the speed performance of the
                   Genetic Algorithm.
      """
      self.dbAdapter = dbadapter

   def setPopulationSize(self, size):
      """ Sets the population size, calls setPopulationSize() of GPopulation

      :param size: the population size

      .. note:: the population size must be >= 2

      """
      if size < 2:
         Util.raiseException("population size must be >= 2", ValueError)
      self.internalPop.setPopulationSize(size)

   def setSortType(self, sort_type):
      """ Sets the sort type, Consts.sortType["raw"]/Consts.sortType["scaled"]

      Example:
         >>> ga_engine.setSortType(Consts.sortType["scaled"])

      :param sort_type: the Sort Type

      """
      if sort_type not in Consts.sortType.values():
         Util.raiseException("sort type must be a Consts.sortType type", TypeError)
      self.internalPop.sortType = sort_type

   def setMutationRate(self, rate):
      """ Sets the mutation rate, between 0.0 and 1.0

      :param rate: the rate, between 0.0 and 1.0

      """
      if (rate>1.0) or (rate<0.0):
         Util.raiseException("Mutation rate must be >= 0.0 and <= 1.0", ValueError)
      self.pMutation = rate

   def setCrossoverRate(self, rate):
      """ Sets the crossover rate, between 0.0 and 1.0

      :param rate: the rate, between 0.0 and 1.0

      """
      if (rate>1.0) or (rate<0.0):
         Util.raiseException("Crossover rate must be >= 0.0 and <= 1.0", ValueError)
      self.pCrossover = rate

   def setGenerations(self, num_gens):
      """ Sets the number of generations to evolve

      :param num_gens: the number of generations

      """
      if num_gens < 1:
         Util.raiseException("Number of generations must be >= 1", ValueError)
      self.nGenerations = num_gens

   def getMinimax(self):
      """ Gets the minimize/maximize mode

      :rtype: the Consts.minimaxType type

      """
      return self.minimax

   def setMinimax(self, mtype):
      """ Sets the minimize/maximize mode, use Consts.minimaxType

      :param mtype: the minimax mode, from Consts.minimaxType

      """
      if mtype not in Consts.minimaxType.values():
         Util.raiseException("Minimax must be maximize or minimize", TypeError)
      self.minimax = mtype

   def getCurrentGeneration(self):
      """ Gets the current generation

      :rtype: the current generation

      """
      return self.currentGeneration

   def setElitism(self, flag):
      """ Sets the elitism option, True or False

      :param flag: True or False

      """
      if type(flag) != BooleanType:
         Util.raiseException("Elitism option must be True or False", TypeError)
      self.elitism = flag

   def getDBAdapter(self):
      """ Gets the DB Adapter of the GA Engine

      :rtype: a instance from one of the :mod:`DBAdapters` classes

      """
      return self.dbAdapter

   def bestIndividual(self):
      """ Returns the population best individual

      :rtype: the best individual

      """
      return self.internalPop.bestRaw()

   def initialize(self):
      """ Initializes the GA Engine. Create and initialize population """
      self.internalPop.create(minimax=self.minimax)
      self.internalPop.initialize()
      logging.debug("The GA Engine was initialized !")      

   def getPopulation(self):
      """ Return the internal population of GA Engine

      :rtype: the population (:class:`GPopulation.GPopulation`)

      """
      return self.internalPop
   
   def getStatistics(self):
      """ Gets the Statistics class instance of current generation

      :rtype: the statistics instance (:class:`Statistics.Statistics`)

      """
      return self.internalPop.getStatistics()

   def step(self):
      """ Just do one step in evolution, one generation """
      genomeMom = None
      genomeDad = None

      newPop = self.internalPop.clone()
      newPop.clear()
      logging.debug("Population was cloned.")
      
      size_iterate = len(self.internalPop)
      if size_iterate % 2 != 0: size_iterate -= 1

      for i in xrange(0, size_iterate, 2):
         genomeMom = self.select(popID=self.currentGeneration)
         genomeDad = self.select(popID=self.currentGeneration)
         
         if  not genomeMom.crossover.isEmpty() and self.pCrossover >= 1.0:
            for it in genomeMom.crossover.applyFunctions(genomeMom, mom=genomeMom, dad=genomeDad, count=2):
               (sister, brother) = it
         else:
            if not genomeMom.crossover.isEmpty() and Util.randomFlipCoin(self.pCrossover):
               for it in genomeMom.crossover.applyFunctions(genomeMom, mom=genomeMom, dad=genomeDad, count=2):
                  (sister, brother) = it
            else:
               sister = genomeMom.clone()
               brother = genomeDad.clone()

         newPop.internalPop.append(sister)
         newPop.internalPop.append(brother)

         for lastInd in newPop.internalPop[-2:]:
            lastInd.mutate(pmut=self.pMutation)

      if len(self.internalPop) % 2 != 0:
         genomeMom = self.select(popID=self.currentGeneration)
         genomeDad = self.select(popID=self.currentGeneration)

         if Util.randomFlipCoin(self.pCrossover):
            for it in genomeMom.crossover.applyFunctions(genomeMom, mom=genomeMom, dad=genomeDad, count=1):
               (sister, brother) = it
         else:
            sister = random.choice([genomeMom, genomeDad])

         newPop.internalPop.append(sister.clone())

      logging.debug("Evaluating the new created population.")
      newPop.evaluate()

      if self.elitism:
         logging.debug("Doing elitism.")
         if self.minimax == Consts.minimaxType["maximize"]:
            if self.internalPop.bestRaw().score > newPop.bestRaw().score:
               newPop[len(newPop)-1] = self.internalPop.bestRaw()
         else:
            if self.internalPop.bestRaw().score < newPop.bestRaw().score:
               newPop[0] = self.internalPop.bestRaw()

      self.internalPop = newPop
      self.internalPop.sort()
      logging.debug("The generation %d was finished.", self.currentGeneration)

      self.currentGeneration += 1

      return (self.currentGeneration == self.nGenerations)
   
   def printStats(self):
      """ Print generation statistics """
      percent = self.currentGeneration * 100 / float(self.nGenerations)
      message = "Gen. %d (%.2f%%):" % (self.currentGeneration, percent)
      logging.info(message)
      print message,
      self.internalPop.statistics()
      self.internalPop.printStats()

   def printTimeElapsed(self):
      """ Shows the time elapsed since the begin of evolution """
      print "Total time elapsed: %.3f seconds." % (time()-self.time_init)
   
   def dumpStatsDB(self):
      """ Dumps the current statistics to database adapter """
      self.internalPop.statistics()
      self.dbAdapter.insert(self.getStatistics(), self.internalPop, self.currentGeneration)

   def evolve(self, freq_stats=0):
      """ Do all the generations until the termination criteria, accepts
      the freq_stats (default is 0) to dump statistics at n-generation

      Example:
         >>> ga_engine.evolve(freq_stats=10)
         (...)

      :param freq_stats: if greater than 0, the statistics will be
                         printed every freq_stats generation.

      """

      self.time_init = time()

      if self.dbAdapter: self.dbAdapter.open()

      self.initialize()
      self.internalPop.evaluate()
      self.internalPop.sort()
      logging.debug("Starting loop over evolutionary algorithm.")


      try:      
         while not self.step():
            stopFlagCallback = False
            stopFlagTerminationCriteria = False

            if not self.stepCallback.isEmpty():
                for it in self.stepCallback.applyFunctions(self):
                  stopFlagCallback = it

            if not self.terminationCriteria.isEmpty():
                for it in self.terminationCriteria.applyFunctions(self):
                  stopFlagTerminationCriteria = it

            if freq_stats != 0:
               if (self.currentGeneration % freq_stats == 0) or (self.currentGeneration == 1):
                  self.printStats()

            if self.dbAdapter:
               if self.currentGeneration % self.dbAdapter.statsGenFreq == 0:
                  self.dumpStatsDB()

            if stopFlagTerminationCriteria:
               logging.debug("Evolution stopped by the Termination Criteria !")
               print "\n\tEvolution stopped by Termination Criteria function !\n"
               break

            if stopFlagCallback:
               logging.debug("Evolution stopped by Step Callback function !")
               print "\n\tEvolution stopped by Step Callback function !\n"
               break


            if self.interactiveMode:

               if sys_platform[:3] == "win":
                  if msvcrt.kbhit():
                     if ord(msvcrt.getch()) == Consts.CDefESCKey:
                        import pyevolve.Interaction
                        interact_banner = "## Pyevolve v.%s - Interactive Mode ##\nPress CTRL-Z to quit interactive mode." % (pyevolve.__version__,)
                        session_locals = { "ga_engine"  : self,
                                           "population" : self.getPopulation(),
                                           "pyevolve"   : pyevolve,
                                           "it"         : pyevolve.Interaction}
                        print
                        code.interact(interact_banner, local=session_locals)
               elif sys_platform[:5] == "linux":
                  if Util.kbhit():
                     if ord(Util.getch()) == Consts.CDefESCKey:
                        import pyevolve.Interaction
                        interact_banner = "## Pyevolve v.%s - Interactive Mode ##\nPress CTRL-D to quit interactive mode." % (pyevolve.__version__,)
                        session_locals = { "ga_engine"  : self,
                                           "population" : self.getPopulation(),
                                           "pyevolve"   : pyevolve,
                                           "it"         : pyevolve.Interaction}
                        print
                        code.interact(interact_banner, local=session_locals)

      except KeyboardInterrupt:
         logging.debug("CTRL-C detected, finishing evolution.")
         print "\n\tA break was detected, you have interrupted the evolution !\n"

      if freq_stats != 0:
         self.printStats()
         self.printTimeElapsed()

      if self.dbAdapter:
         if not (self.currentGeneration % self.dbAdapter.statsGenFreq == 0):
            self.dumpStatsDB()
         self.dbAdapter.commitAndClose()

   def select(self, **args):
      """ Select one individual from population

      :param args: this parameters will be sent to the selector

      """
      for it in self.selector.applyFunctions(self.internalPop, **args):
         return it

