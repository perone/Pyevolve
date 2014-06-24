"""
:mod:`Migration` -- the migration schemes, distributed GA
=====================================================================

This module contains all the migration schemes and the distributed
GA related functions.

.. versionadded:: 0.6
   The :mod:`Migration` module.

"""

import Util
from random import randint as rand_randint, choice as rand_choice
import Network
import Consts
from FunctionSlot import FunctionSlot
import logging

try:
   from mpi4py import MPI
   HAS_MPI4PY = True
except ImportError:
   HAS_MPI4PY = False

class MigrationScheme(object):
   """ This is the base class for all migration schemes """

   selector = None
   """ This is the function slot for the selection method
   if you want to change the default selector, you must do this: ::

      migration_scheme.selector.set(Selectors.GRouletteWheel) """

   def __init__(self):
      self.selector = FunctionSlot("Selector")
      self.GAEngine = None
      self.nMigrationRate = Consts.CDefGenMigrationRate
      self.nIndividuals = Consts.CDefMigrationNIndividuals
      self.nReplacement = Consts.CDefGenMigrationReplacement
      self.networkCompression = 9

   def isReady(self):
      """ Returns true if is time to migrate """
      return True if self.GAEngine.getCurrentGeneration() % self.nMigrationRate == 0 else False

   def getCompressionLevel(self):
      """ Get the zlib compression level of network data

      The values are in the interval described on the :func:`Network.pickleAndCompress`
      """
      return self.networkCompression

   def setCompressionLevel(self, level):
      """ Set the zlib compression level of network data

      The values are in the interval described on the :func:`Network.pickleAndCompress`

      :param level: the zlib compression level
      """
      self.networkCompression = level

   def getNumReplacement(self):
      """ Return the number of individuals that will be
      replaced in the migration process """
      return self.nReplacement

   def setNumReplacement(self, num_individuals):
      """ Return the number of individuals that will be
      replaced in the migration process

      :param num_individuals: the number of individuals to be replaced
      """
      self.nReplacement = num_individuals

   def getNumIndividuals(self):
      """ Return the number of individuals that will migrate

      :rtype: the number of individuals to be replaced
      """
      return self.nIndividuals

   def setNumIndividuals(self, num_individuals):
      """ Set the number of individuals that will migrate

      :param num_individuals: the number of individuals
      """
      self.nIndividuals = num_individuals

   def setMigrationRate(self, generations):
      """ Sets the generation frequency supposed to migrate
      and receive individuals.

      :param generations: the number of generations
      """
      self.nMigrationRate = generations

   def getMigrationRate(self):
      """ Return the the generation frequency supposed to migrate
      and receive individuals

      :rtype: the number of generations
      """
      return self.nMigrationRate

   def setGAEngine(self, ga_engine):
      """ Sets the GA Engine handler """
      self.GAEngine = ga_engine

   def start(self):
      """ Initializes the migration scheme """
      pass

   def stop(self):
      """ Stops the migration engine """
      pass

   def select(self):
      """ Picks an individual from population using specific selection method

      :rtype: an individual object
      """
      if self.selector.isEmpty():
         return self.GAEngine.select(popID=self.GAEngine.currentGeneration)
      else:
         for it in self.selector.applyFunctions(self.GAEngine.internalPop,
                                                popID=self.GAEngine.currentGeneration):
            return it

   def selectPool(self, num_individuals):
      """ Select num_individuals number of individuals and return a pool

      :param num_individuals: the number of individuals to select
      :rtype: list with individuals
      """
      pool = [self.select() for i in xrange(num_individuals)]
      return pool

   def exchange(self):
      """ Exchange individuals """
      pass


class WANMigration(MigrationScheme):
   """ This is the Simple Migration class for distributed GA

   Example:
      >>> mig = WANMigration("192.168.0.1", "10000", "group1")

   :param host: the source hostname
   :param port: the source port number
   :param group_name: the group name
   """

   selector = None
   """ This is the function slot for the selection method
   if you want to change the default selector, you must do this: ::

      migration_scheme.selector.set(Selectors.GRouletteWheel) """

   def __init__(self, host, port, group_name):
      super(WANMigration, self).__init__()
      self.setMyself(host, port)
      self.setGroupName(group_name)
      self.topologyGraph = None
      self.serverThread = Network.UDPThreadServer(host, port)
      self.clientThread = Network.UDPThreadUnicastClient(self.myself[0], rand_randint(30000, 65534))

   def setMyself(self, host, port):
      """ Which interface you will use to send/receive data

      :param host: your hostname
      :param port: your port
      """
      self.myself = (host, port)

   def getGroupName(self):
      """ Gets the group name

      .. note:: all islands of evolution which are supposed to exchange
                individuals, must have the same group name.
      """
      return self.groupName

   def setGroupName(self, name):
      """ Sets the group name

      :param name: the group name

      .. note:: all islands of evolution which are supposed to exchange
                individuals, must have the same group name.
      """
      self.groupName = name

   def setTopology(self, graph):
      """ Sets the topology of the migrations

      :param graph: the :class:`Util.Graph` instance
      """
      self.topologyGraph = graph

   def start(self):
      """ Start capture of packets and initialize the migration scheme """
      self.serverThread.start()

      if self.topologyGraph is None:
         Util.raiseException("You must add a topology graph to the migration scheme !")

      targets = self.topologyGraph.getNeighbors(self.myself)
      self.clientThread.setMultipleTargetHost(targets)
      self.clientThread.start()

   def stop(self):
      """ Stops the migration engine """
      self.serverThread.shutdown()
      self.clientThread.shutdown()
      server_timeout = self.serverThread.timeout
      client_timeout = self.clientThread.timeout

      self.serverThread.join(server_timeout + 3)
      self.clientThread.join(client_timeout + 3)

      if self.serverThread.isAlive():
         logging.warning("warning: server thread not joined !")

      if self.clientThread.isAlive():
         logging.warning("warning: client thread not joined !")

   def exchange(self):
      """ This is the main method, is where the individuals
      are exchanged """

      if not self.isReady():
         return

      # Client section --------------------------------------
      # How many will migrate ?
      pool = self.selectPool(self.getNumIndividuals())

      for individual in pool:
         # (code, group name, individual)
         networkObject = (Consts.CDefNetworkIndividual, self.getGroupName(), individual)
         networkData = Network.pickleAndCompress(networkObject, self.getCompressionLevel())
         # Send the individuals to the topology
         self.clientThread.addData(networkData)

      # Server section --------------------------------------
      pool = []
      while self.serverThread.isReady():
         # (IP source, data)
         networkData = self.serverThread.popPool()
         networkObject = Network.unpickleAndDecompress(networkData[1])
         # (code, group name, individual)
         pool.append(networkObject)

      # No individuals received
      if len(pool) <= 0:
         return

      population = self.GAEngine.getPopulation()

      for i in xrange(self.getNumReplacement()):
         if len(pool) <= 0:
            break
         choice = rand_choice(pool)
         pool.remove(choice)

         # replace the worst
         population[len(population) - 1 - i] = choice[2]


class MPIMigration(MigrationScheme):
   """ This is the MPIMigration """

   def __init__(self):
      # Delayed ImportError of mpi4py
      if not HAS_MPI4PY:
         raise ImportError("No module named mpi4py, you must install mpi4py to use MPIMIgration!")

      super(MPIMigration, self).__init__()

      self.comm = MPI.COMM_WORLD
      self.pid = self.comm.rank

      if self.pid == 0:
         self.source = self.comm.size - 1
      else:
         self.source = self.comm.rank - 1

      self.dest = (self.comm.rank + 1) % (self.comm.size)

      self.all_stars = None

   def isReady(self):
      """ Returns true if is time to migrate """

      if self.GAEngine.getCurrentGeneration() == 0:
         return False

      if self.GAEngine.getCurrentGeneration() % self.nMigrationRate == 0:
         return True
      else:
         return False

   def gather_bests(self):
      '''
      Collect all the best individuals from the various populations. The
      result is stored in process 0
      '''
      best_guy = self.select()
      self.all_stars = self.comm.gather(sendobj=best_guy, root=0)

   def exchange(self):
      """ This is the main method, is where the individuals
      are exchanged """

      if not self.isReady():
         return

      pool_to_send = self.selectPool(self.getNumIndividuals())
      pool_received = self.comm.sendrecv(sendobj=pool_to_send,
                                         dest=self.dest,
                                         sendtag=0,
                                         recvobj=None,
                                         source=self.source,
                                         recvtag=0)

      population = self.GAEngine.getPopulation()

      pool = pool_received
      for i in xrange(self.getNumReplacement()):
         if len(pool) <= 0:
            break

         choice = rand_choice(pool)
         pool.remove(choice)

         # replace the worst
         population[len(population) - 1 - i] = choice

      self.gather_bests()
