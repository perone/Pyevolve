"""

:mod:`Util` -- utility module
============================================================================

This is the utility module, with some utility functions of general
use, like list item swap, random utilities and etc.

"""

from random import random as rand_random
from math import sqrt as math_sqrt
import logging
import Consts

def randomFlipCoin(p):
   """ Returns True with the *p* probability. If the *p* is 1.0,
   the function will always return True, or if is 0.0, the
   function will return always False.
   
   Example:
      >>> Util.randomFlipCoin(1.0)
      True

   :param p: probability, between 0.0 and 1.0
   :rtype: True or False

   """
   if p == 1.0: return True
   if p == 0.0: return False

   return True if rand_random() <= p else False
   
def listSwapElement(lst, indexa, indexb):
   """ Swaps elements A and B in a list.

   Example:
      >>> l = [1, 2, 3]
      >>> Util.listSwapElement(l, 1, 2)
      >>> l
      [1, 3, 2]

   :param lst: the list
   :param indexa: the swap element A
   :param indexb: the swap element B
   :rtype: None

   """
   lst[indexa], lst[indexb] = lst[indexb], lst[indexa]

def list2DSwapElement(lst, indexa, indexb):
   """ Swaps elements A and B in a 2D list (matrix).

   Example:
      >>> l = [ [1,2,3], [4,5,6] ] 
      >>> Util.list2DSwapElement(l, (0,1), (1,1) )
      >>> l
      [[1, 5, 3], [4, 2, 6]]

   :param lst: the list
   :param indexa: the swap element A
   :param indexb: the swap element B
   :rtype: None

   """
   temp = lst[indexa[0]][indexa[1]]
   lst[indexa[0]][indexa[1]] = lst[indexb[0]][indexb[1]]
   lst[indexb[0]][indexb[1]] = temp

def raiseException(message, expt=None):
   """ Raise an exception and logs the message.

   Example:
      >>> Util.raiseException('The value is not an integer', ValueError)

   :param message: the message of exception
   :param expt: the exception class
   :rtype: None

   """
   logging.critical(message)
   if expt is None:
      raise Exception(message)
   else:
      raise expt, message


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

def importSpecial(name):
   """ This function will import the *name* module, if fails,
   it will raise an ImportError exception and a message

   :param name: the module name
   :rtype: the module object
   
   .. versionadded:: 0.6
      The *import_special* function
   """
   try:
      imp_mod = __import__(name)
   except ImportError:
      raiseException("Cannot import module %s: %s" % (name, Consts.CDefImportList[name]), expt=ImportError)
   return imp_mod 

class ErrorAccumulator:
   """ An accumulator for the Root Mean Square Error (RMSE) and the
   Mean Square Error (MSE)
   """
   def __init__(self):
      self.acc        = 0.0
      self.acc_square = 0.0
      self.acc_len    = 0

   def reset(self):
      """ Reset the accumulator """
      self.acc_square = 0.0
      self.acc        = 0.0
      self.acc_len    = 0

   def append(self, target, evaluated):
      """ Add value to the accumulator
      
      :param target: the target value
      :param evaluated: the evaluated value
      """
      self.acc_square += (target - evaluated)**2
      self.acc        += (target - evaluated)
      self.acc_len    +=1
      
   def __iadd__(self, value):
      """ The same as append, but you must pass a tuple """
      self.acc_square += (value[0] - value[1])**2
      self.acc        += abs(value[0] - value[1])
      self.acc_len    +=1
      return self

   def getMean(self):
      """ Return the mean of the non-squared accumulator """
      return self.acc / self.acc_len

   def getSquared(self):
      """ Returns the squared accumulator """
      return self.acc_square

   def getNonSquared(self):
      """ Returns the non-squared accumulator """
      return self.acc

   def getAdjusted(self):
      """ Returns the adjusted fitness
      This fitness is calculated as 1 / (1 + standardized fitness)
      """
      return 1.0/(1.0 + self.acc)

   def getRMSE(self):
      """ Return the root mean square error
      
      :rtype: float RMSE
      """
      return math_sqrt(self.acc_square / float(self.acc_len))

   def getMSE(self):
      """ Return the mean square error

      :rtype: float MSE
      """
      return (self.acc_square / float(self.acc_len))


class Graph:
   """ The Graph class

   Example:
      >>> g = Graph()
      >>> g.addEdge("a", "b")
      >>> g.addEdge("b", "c")
      >>> for node in g:
      ...    print node
      a
      b
      c
   
   .. versionadded:: 0.6
      The *Graph* class.
   """

   def __init__(self):
      """ The constructor """
      self.adjacent = {}

   def __iter__(self):
      """ Returns an iterator to the all graph elements """
      return iter(self.adjacent)

   def addNode(self, node):
      """ Add the node

      :param node: the node to add
      """
      if node not in self.adjacent:
         self.adjacent[node] = {}

   def __iadd__(self, node):
      """ Add a node using the += operator """
      self.addNode(node)
      return self

   def addEdge(self, a, b):
      """ Add an edge between two nodes, if the nodes
      doesn't exists, they will be created
      
      :param a: the first node
      :param b: the second node
      """
      if a not in self.adjacent: 
         self.adjacent[a] = {}

      if b not in self.adjacent: 
         self.adjacent[b] = {}

      self.adjacent[a][b] = True
      self.adjacent[b][a] = True

   def getNodes(self):
      """ Returns all the current nodes on the graph
      
      :rtype: the list of nodes
      """
      return self.adjacent.keys()

   def reset(self):
      """ Deletes all nodes of the graph """
      self.adjacent.clear() 

   def getNeighbors(self, node):
      """ Returns the neighbors of the node
      
      :param node: the node
      """
      return self.adjacent[node].keys()

   def __getitem__(self, node):
      """ Returns the adjacent nodes of the node """
      return self.adjacent[node].keys()

   def __repr__(self):
      ret =  "- Graph\n"
      ret += "\tNode list:\n"
      for node in self:
         ret += "\t\tNode [%s] = %s\n" % (node, self.getNeighbors(node))
      return ret         
      

def G1DListGetEdgesComposite(mom, dad):
   """ Get the edges and the merge between the edges of two G1DList individuals

   :param mom: the mom G1DList individual
   :param dad: the dad G1DList individual
   :rtype: a tuple (mom edges, dad edges, merge)
   """
   mom_edges = G1DListGetEdges(mom)
   dad_edges = G1DListGetEdges(dad)
   return (mom_edges, dad_edges, G1DListMergeEdges(mom_edges, dad_edges))

def G1DListGetEdges(individual):
   """ Get the edges of a G1DList individual 

   :param individual: the G1DList individual
   :rtype: the edges dictionary
   """
   edg = {}
   ind_list = individual.getInternalList()
   for i in xrange(len(ind_list)):
      a, b = ind_list[i], ind_list[i-1]

      if a not in edg: edg[a] = []
      else: edg[a].append(b)

      if b not in edg: edg[b] = []
      else: edg[b].append(a)
   return edg
 
def G1DListMergeEdges(eda, edb):
   """ Get the merge between the two individual edges

   :param eda: the edges of the first G1DList genome
   :param edb: the edges of the second G1DList genome
   :rtype: the merged dictionary
   """
   edges = {}
   for value, near in eda.items():
      for adj in near:
         if (value in edb) and (adj in edb[value]):
            edges.setdefault(value, []).append(adj)
   return edges
