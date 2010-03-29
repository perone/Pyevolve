"""

:mod:`GSimpleGA` -- the genetic algorithm by itself
=====================================================================

This module contains the GA Engine, the GA Engine class is responsible
for all the evolutionary process. It contains the GA Engine related
funtions, like the Termination Criteria functions for convergence analysis, etc.

Default Parameters
-------------------------------------------------------------

*Number of Generations*
  
   Default is 100 generations

*Mutation Rate*
   
   Default is 0.02, which represents 0.2%

*Crossover Rate*

   Default is 0.9, which represents 90%

*Elitism Replacement*

   Default is 1 individual

*Population Size*

   Default is 80 individuals

*Minimax*

   >>> Consts.minimaxType["maximize"]

   Maximize the evaluation function

*DB Adapter*

   Default is **None**

*Migration Adapter*

   Default is **None**
   
*Interactive Mode*

   Default is **True**

*Selector (Selection Method)*

   :func:`Selectors.GRankSelector`

   The Rank Selection method

Class
-------------------------------------------------------------

"""

from GPopulation  import GPopulation
from FunctionSlot import FunctionSlot
from Migration    import MigrationScheme
from GenomeBase   import GenomeBase
from DBAdapters   import DBBaseAdapter

import Consts
import Util

import random
import logging

from time  import time
from types import BooleanType
from sys   import platform as sys_platform
from sys   import stdout as sys_stdout

import code
import pyevolve

# Platform dependant code for the Interactive Mode
if sys_platform[:3] == "win":
   import msvcrt

def RawScoreCriteria(ga_engine):
   """ Terminate the evolution using the **bestrawscore** and **rounddecimal**
   parameter obtained from the individual

   Example:
      >>> genome.setParams(bestrawscore=0.00, rounddecimal=2)
      (...)
      >>> ga_engine.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

   """
   ind = ga_engine.bestIndividual()
   bestRawScore = ind.getParam("bestrawscore")
   roundDecimal = ind.getParam("rounddecimal")

   if bestRawScore is None:
      Util.raiseException("you must specify the bestrawscore parameter", ValueError)

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

   .. note:: if you use the same random seed, all the runs of algorithm will be the same

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
      if seed: random.seed(seed)

      if type(interactiveMode) != BooleanType:
         Util.raiseException("Interactive Mode option must be True or False", TypeError)
      
      if not isinstance(genome, GenomeBase):
         Util.raiseException("The genome must be a GenomeBase subclass", TypeError)

      self.internalPop  = GPopulation(genome)
      self.nGenerations = Consts.CDefGAGenerations
      self.pMutation    = Consts.CDefGAMutationRate
      self.pCrossover   = Consts.CDefGACrossoverRate
      self.nElitismReplacement = Consts.CDefGAElitismReplacement
      self.setPopulationSize(Consts.CDefGAPopulationSize)
      self.minimax      = Consts.minimaxType["maximize"]
      self.elitism      = True

      # Adapters
      self.dbAdapter        = None
      self.migrationAdapter = None
      
      self.time_init       = None
      self.interactiveMode = interactiveMode
      self.interactiveGen  = -1
      self.GPMode = False

      self.selector            = FunctionSlot("Selector")
      self.stepCallback        = FunctionSlot("Generation Step Callback")
      self.terminationCriteria = FunctionSlot("Termination Criteria")
      self.selector.set(Consts.CDefGASelector)
      self.allSlots            = [ self.selector, self.stepCallback, self.terminationCriteria ]

      self.internalParams = {}

      self.currentGeneration = 0

      # GP Testing
      for classes in Consts.CDefGPGenomes:
         if  isinstance(self.internalPop.oneSelfGenome, classes):
            self.setGPMode(True)
            break
      
      logging.debug("A GA Engine was created, nGenerations=%d", self.nGenerations)

   def setGPMode(self, bool_value):
      """ Sets the Genetic Programming mode of the GA Engine
      
      :param bool_value: True or False
      """
      self.GPMode = bool_value

   def getGPMode(self):
      """ Get the Genetic Programming mode of the GA Engine
      
      :rtype: True or False
      """
      return self.GPMode

   def __call__(self, *args, **kwargs):
      """ A method to implement a callable object

      Example:
         >>> ga_engine(freq_stats=10)
         
      .. versionadded:: 0.6
         The callable method.
      """
      if kwargs.get("freq_stats", None):
         return self.evolve(kwargs.get("freq_stats"))
      else:
         return self.evolve()

   def setParams(self, **args):
      """ Set the internal params

      Example:
         >>> ga.setParams(gp_terminals=['x', 'y'])


      :param args: params to save

      ..versionaddd:: 0.6
         Added the *setParams* method.
      """
      self.internalParams.update(args)
   
   def getParam(self, key, nvl=None):
      """ Gets an internal parameter

      Example:
         >>> ga.getParam("gp_terminals")
         ['x', 'y']

      :param key: the key of param
      :param nvl: if the key doesn't exist, the nvl will be returned

      ..versionaddd:: 0.6
         Added the *getParam* method.
      """
      return self.internalParams.get(key, nvl)

   def setInteractiveGeneration(self, generation):
      """ Sets the generation in which the GA must enter in the
      Interactive Mode
      
      :param generation: the generation number, use "-1" to disable

      .. versionadded::0.6
         The *setInteractiveGeneration* method.
      """
      if generation < -1:
         Util.raiseException("Generation must be >= -1", ValueError)
      self.interactiveGen = generation

   def getInteractiveGeneration(self):
      """ returns the generation in which the GA must enter in the
      Interactive Mode
      
      :rtype: the generation number or -1 if not set

      .. versionadded::0.6
         The *getInteractiveGeneration* method.
      """
      return self.interactiveGen

   def setElitismReplacement(self, numreplace):
      """ Set the number of best individuals to copy to the next generation on the elitism

      :param numreplace: the number of individuals
      
      .. versionadded:: 0.6
         The *setElitismReplacement* method.

      """
      if numreplace < 1:
         Util.raiseException("Replacement number must be >= 1", ValueError)
      self.nElitismReplacement = numreplace


   def setInteractiveMode(self, flag=True):
      """ Enable/disable the interactive mode
      
      :param flag: True or False

      .. versionadded: 0.6
         The *setInteractiveMode* method.
      
      """
      if type(flag) != BooleanType:
         Util.raiseException("Interactive Mode option must be True or False", TypeError)
      self.interactiveMode = flag


   def __repr__(self):
      """ The string representation of the GA Engine """
      ret =  "- GSimpleGA\n"
      ret += "\tGP Mode:\t\t %s\n" % self.getGPMode()
      ret += "\tPopulation Size:\t %d\n" % (self.internalPop.popSize,)
      ret += "\tGenerations:\t\t %d\n" % (self.nGenerations,)
      ret += "\tCurrent Generation:\t %d\n" % (self.currentGeneration,)
      ret += "\tMutation Rate:\t\t %.2f\n" % (self.pMutation,)
      ret += "\tCrossover Rate:\t\t %.2f\n" % (self.pCrossover,)
      ret += "\tMinimax Type:\t\t %s\n" % (Consts.minimaxType.keys()[Consts.minimaxType.values().index(self.minimax)].capitalize(),)
      ret += "\tElitism:\t\t %s\n" % (self.elitism,)
      ret += "\tElitism Replacement:\t %d\n" % (self.nElitismReplacement,)
      ret += "\tDB Adapter:\t\t %s\n" % (self.dbAdapter,)
      for slot in self.allSlots:
         ret+= "\t" + slot.__repr__()
      ret+="\n"
      return ret
   
   def setMultiProcessing(self, flag=True, full_copy=False):
      """ Sets the flag to enable/disable the use of python multiprocessing module.
      Use this option when you have more than one core on your CPU and when your
      evaluation function is very slow.

      Pyevolve will automaticly check if your Python version has **multiprocessing**
      support and if you have more than one single CPU core. If you don't have support
      or have just only one core, Pyevolve will not use the **multiprocessing**
      feature.

      Pyevolve uses the **multiprocessing** to execute the evaluation function over
      the individuals, so the use of this feature will make sense if you have a
      truly slow evaluation function (which is commom in GAs).      

      The parameter "full_copy" defines where the individual data should be copied back
      after the evaluation or not. This parameter is useful when you change the
      individual in the evaluation function.
      
      :param flag: True (default) or False
      :param full_copy: True or False (default)

      .. warning:: Use this option only when your evaluation function is slow, so you'll
                   get a good tradeoff between the process communication speed and the
                   parallel evaluation. The use of the **multiprocessing** doesn't means
                   always a better performance.

      .. note:: To enable the multiprocessing option, you **MUST** add the *__main__* check
                on your application, otherwise, it will result in errors. See more on the
                `Python Docs <http://docs.python.org/library/multiprocessing.html#multiprocessing-programming>`__
                site.

      .. versionadded:: 0.6
         The `setMultiProcessing` method.

      """
      if type(flag) != BooleanType:
         Util.raiseException("Multiprocessing option must be True or False", TypeError)

      if type(full_copy) != BooleanType:
         Util.raiseException("Multiprocessing 'full_copy' option must be True or False", TypeError)

      self.internalPop.setMultiProcessing(flag, full_copy)

   def setMigrationAdapter(self, migration_adapter=None):
      """ Sets the Migration Adapter

      .. versionadded:: 0.6
         The `setMigrationAdapter` method.
      """
      if (migration_adapter is not None) and (not isinstance(migration_adapter, MigrationScheme)):
         Util.raiseException("The Migration Adapter must be a MigrationScheme subclass", TypeError)

      self.migrationAdapter = migration_adapter
      if self.migrationAdapter is not None:
         self.migrationAdapter.setGAEngine(self)

   def setDBAdapter(self, dbadapter=None):
      """ Sets the DB Adapter of the GA Engine
      
      :param dbadapter: one of the :mod:`DBAdapters` classes instance

      .. warning:: the use the of a DB Adapter can reduce the speed performance of the
                   Genetic Algorithm.
      """
      if (dbadapter is not None) and (not isinstance(dbadapter, DBBaseAdapter)):
         Util.raiseException("The DB Adapter must be a DBBaseAdapter subclass", TypeError)
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

   def getGenerations(self):
      """ Return the number of generations to evolve

      :rtype: the number of generations

      .. versionadded:: 0.6
         Added the *getGenerations* method
      """
      return self.nGenerations

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

   def __gp_catch_functions(self, prefix):
      """ Internally used to catch functions with some specific prefix
      as non-terminals of the GP core """
      import __main__ as mod_main

      function_set = {}

      main_dict = mod_main.__dict__
      for obj, addr in main_dict.items():
         if obj[0:len(prefix)] == prefix:
            try:
               op_len = addr.func_code.co_argcount
            except:
               continue
            function_set[obj] = op_len

      if len(function_set) <= 0:
         Util.raiseException("No function set found using function prefix '%s' !" % prefix, ValueError)

      self.setParams(gp_function_set=function_set)

   def initialize(self):
      """ Initializes the GA Engine. Create and initialize population """
      self.internalPop.create(minimax=self.minimax)
      self.internalPop.initialize(ga_engine=self)
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

   
   def clear(self):
      """ Petrowski's Clearing Method """
      

   def step(self):
      """ Just do one step in evolution, one generation """
      genomeMom = None
      genomeDad = None

      newPop = GPopulation(self.internalPop)
      logging.debug("Population was cloned.")
      
      size_iterate = len(self.internalPop)

      # Odd population size
      if size_iterate % 2 != 0: size_iterate -= 1

      crossover_empty = self.select(popID=self.currentGeneration).crossover.isEmpty()
      
      for i in xrange(0, size_iterate, 2):
         genomeMom = self.select(popID=self.currentGeneration)
         genomeDad = self.select(popID=self.currentGeneration)
         
         if not crossover_empty and self.pCrossover >= 1.0:
            for it in genomeMom.crossover.applyFunctions(mom=genomeMom, dad=genomeDad, count=2):
               (sister, brother) = it
         else:
            if not crossover_empty and Util.randomFlipCoin(self.pCrossover):
               for it in genomeMom.crossover.applyFunctions(mom=genomeMom, dad=genomeDad, count=2):
                  (sister, brother) = it
            else:
               sister = genomeMom.clone()
               brother = genomeDad.clone()

         sister.mutate(pmut=self.pMutation, ga_engine=self)
         brother.mutate(pmut=self.pMutation, ga_engine=self)

         newPop.internalPop.append(sister)
         newPop.internalPop.append(brother)

      if len(self.internalPop) % 2 != 0:
         genomeMom = self.select(popID=self.currentGeneration)
         genomeDad = self.select(popID=self.currentGeneration)

         if Util.randomFlipCoin(self.pCrossover):
            for it in genomeMom.crossover.applyFunctions(mom=genomeMom, dad=genomeDad, count=1):
               (sister, brother) = it
         else:
            sister = random.choice([genomeMom, genomeDad])
            sister = sister.clone()
            sister.mutate(pmut=self.pMutation, ga_engine=self)

         newPop.internalPop.append(sister)

      logging.debug("Evaluating the new created population.")
      newPop.evaluate()

      #Niching methods- Petrowski's clearing
      self.clear()

      if self.elitism:
         logging.debug("Doing elitism.")
         if self.getMinimax() == Consts.minimaxType["maximize"]:
            for i in xrange(self.nElitismReplacement):
               if self.internalPop.bestRaw(i).score > newPop.bestRaw(i).score:
                  newPop[len(newPop)-1-i] = self.internalPop.bestRaw(i)
         elif self.getMinimax() == Consts.minimaxType["minimize"]:
            for i in xrange(self.nElitismReplacement):
               if self.internalPop.bestRaw(i).score < newPop.bestRaw(i).score:
                  newPop[len(newPop)-1-i] = self.internalPop.bestRaw(i)

      self.internalPop = newPop
      self.internalPop.sort()

      logging.debug("The generation %d was finished.", self.currentGeneration)

      self.currentGeneration += 1

      return (self.currentGeneration == self.nGenerations)
   
   def printStats(self):
      """ Print generation statistics

      :rtype: the printed statistics as string

      .. versionchanged:: 0.6
         The return of *printStats* method.
      """
      percent = self.currentGeneration * 100 / float(self.nGenerations)
      message = "Gen. %d (%.2f%%):" % (self.currentGeneration, percent)
      logging.info(message)
      print message,
      sys_stdout.flush()
      self.internalPop.statistics()
      stat_ret = self.internalPop.printStats()
      return message + stat_ret

   def printTimeElapsed(self):
      """ Shows the time elapsed since the begin of evolution """
      total_time = time()-self.time_init
      print "Total time elapsed: %.3f seconds." % total_time
      return total_time
   
   def dumpStatsDB(self):
      """ Dumps the current statistics to database adapter """
      logging.debug("Dumping stats to the DB Adapter")
      self.internalPop.statistics()
      self.dbAdapter.insert(self)

   def evolve(self, freq_stats=0):
      """ Do all the generations until the termination criteria, accepts
      the freq_stats (default is 0) to dump statistics at n-generation

      Example:
         >>> ga_engine.evolve(freq_stats=10)
         (...)

      :param freq_stats: if greater than 0, the statistics will be
                         printed every freq_stats generation.
      :rtype: returns the best individual of the evolution

      .. versionadded:: 0.6
         the return of the best individual

      """

      stopFlagCallback = False
      stopFlagTerminationCriteria = False

      self.time_init = time()

      logging.debug("Starting the DB Adapter and the Migration Adapter if any")
      if self.dbAdapter: self.dbAdapter.open(self)
      if self.migrationAdapter: self.migrationAdapter.start()


      if self.getGPMode():
         gp_function_prefix = self.getParam("gp_function_prefix")
         if gp_function_prefix is not None:
            self.__gp_catch_functions(gp_function_prefix)

      self.initialize()
      self.internalPop.evaluate()
      self.internalPop.sort()
      logging.debug("Starting loop over evolutionary algorithm.")

      try:      
         while True:
            if self.migrationAdapter:
               logging.debug("Migration adapter: exchange")
               self.migrationAdapter.exchange()
               self.internalPop.clearFlags()
               self.internalPop.sort()

            if not self.stepCallback.isEmpty():
               for it in self.stepCallback.applyFunctions(self):
                  stopFlagCallback = it

            if not self.terminationCriteria.isEmpty():
               for it in self.terminationCriteria.applyFunctions(self):
                  stopFlagTerminationCriteria = it

            if freq_stats:
               if (self.currentGeneration % freq_stats == 0) or (self.getCurrentGeneration() == 0):
                  self.printStats()

            if self.dbAdapter:
               if self.currentGeneration % self.dbAdapter.getStatsGenFreq() == 0:
                  self.dumpStatsDB()

            if stopFlagTerminationCriteria:
               logging.debug("Evolution stopped by the Termination Criteria !")
               if freq_stats:
                  print "\n\tEvolution stopped by Termination Criteria function !\n"
               break

            if stopFlagCallback:
               logging.debug("Evolution stopped by Step Callback function !")
               if freq_stats:
                  print "\n\tEvolution stopped by Step Callback function !\n"
               break

            if self.interactiveMode:
               if sys_platform[:3] == "win":
                  if msvcrt.kbhit():
                     if ord(msvcrt.getch()) == Consts.CDefESCKey:
                        print "Loading modules for Interactive Mode...",
                        logging.debug("Windows Interactive Mode key detected ! generation=%d", self.getCurrentGeneration())
                        from pyevolve import Interaction
                        print " done !"
                        interact_banner = "## Pyevolve v.%s - Interactive Mode ##\nPress CTRL-Z to quit interactive mode." % (pyevolve.__version__,)
                        session_locals = { "ga_engine"  : self,
                                           "population" : self.getPopulation(),
                                           "pyevolve"   : pyevolve,
                                           "it"         : Interaction}
                        print
                        code.interact(interact_banner, local=session_locals)

               if (self.getInteractiveGeneration() >= 0) and (self.getInteractiveGeneration() == self.getCurrentGeneration()):
                        print "Loading modules for Interactive Mode...",
                        logging.debug("Manual Interactive Mode key detected ! generation=%d", self.getCurrentGeneration())
                        from pyevolve import Interaction
                        print " done !"
                        interact_banner = "## Pyevolve v.%s - Interactive Mode ##" % (pyevolve.__version__,)
                        session_locals = { "ga_engine"  : self,
                                           "population" : self.getPopulation(),
                                           "pyevolve"   : pyevolve,
                                           "it"         : Interaction}
                        print
                        code.interact(interact_banner, local=session_locals)

            if self.step(): break #exit if the number of generations is equal to the max. number of gens.

      except KeyboardInterrupt:
         logging.debug("CTRL-C detected, finishing evolution.")
         if freq_stats: print "\n\tA break was detected, you have interrupted the evolution !\n"

      if freq_stats != 0:
         self.printStats()
         self.printTimeElapsed()

      if self.dbAdapter:
         logging.debug("Closing the DB Adapter")
         if not (self.currentGeneration % self.dbAdapter.getStatsGenFreq() == 0):
            self.dumpStatsDB()
         self.dbAdapter.commitAndClose()
   
      if self.migrationAdapter:
         logging.debug("Closing the Migration Adapter")
         if freq_stats: print "Stopping the migration adapter... ",
         self.migrationAdapter.stop()
         if freq_stats: print "done !"

      return self.bestIndividual()

   def select(self, **args):
      """ Select one individual from population

      :param args: this parameters will be sent to the selector

      """
      for it in self.selector.applyFunctions(self.internalPop, **args):
         return it

