"""
:mod:`G2DBinaryString` -- the classical binary string chromosome
=====================================================================

This representation is a 2D Binary String, the string looks like
this matrix:

00101101010
00100011010
00101101010
10100101000

Default Parameters
-------------------------------------------------------------

*Initializator*
   
   :func:`Initializators.G2DBinaryStringInitializator`

   The Binatry String Initializator for G2DBinaryString

*Mutator*

   :func:`Mutators.G2DBinaryStringMutatorFlip`

   The Flip Mutator for G2DBinaryString

*Crossover*

   :func:`Crossovers.G2DBinaryStringXSinglePoint`

   The Single Point Crossover for G2DBinaryString

.. versionadded:: 0.6
   Added the module :mod:`G2DBinaryString`

Class
-------------------------------------------------------------
"""

from GenomeBase import GenomeBase
import Consts
import Util
    
class G2DBinaryString(GenomeBase):
   """ G3DBinaryString Class - The 2D Binary String chromosome
   
   Inheritance diagram for :class:`G2DBinaryString.G2DBinaryString`:

   .. inheritance-diagram:: G2DBinaryString.G2DBinaryString

   Example:
      >>> genome = G2DBinaryString.G2DBinaryString(10, 12)


   :param height: the number of rows
   :param width: the number of columns

   """

   evaluator = None
   """ This is the :term:`evaluation function` slot, you can add
   a function with the *set* method: ::

      genome.evaluator.set(eval_func)
   """

   initializator = None
   """ This is the initialization function of the genome, you
   can change the default initializator using the function slot: ::

      genome.initializator.set(Initializators.G2DBinaryStringInitializator)

   In this example, the initializator :func:`Initializators.G1DBinaryStringInitializator`
   will be used to create the initial population.
   """

   mutator = None
   """ This is the mutator function slot, you can change the default
   mutator using the slot *set* function: ::

      genome.mutator.set(Mutators.G2DBinaryStringMutatorSwap)

   """

   crossover = None
   """ This is the reproduction function slot, the crossover. You
   can change the default crossover method using: ::

      genome.crossover.set(Crossovers.G2DBinaryStringXUniform)
   """


   def __init__(self, height, width):
      """ The initializator of G2DBinaryString representation,
      height and width must be specified """
      GenomeBase.__init__(self)
      self.height = height
      self.width = width

      self.genomeString = [None]*height
      for i in xrange(height):
         self.genomeString[i] = [None] * width

      self.initializator.set(Consts.CDefG2DBinaryStringInit)
      self.mutator.set(Consts.CDefG2DBinaryStringMutator)
      self.crossover.set(Consts.CDefG2DBinaryStringCrossover)
   
   def __eq__(self, other):
      """ Compares one chromosome with another """
      cond1 = (self.genomeString == other.genomeString)
      cond2 = (self.height     == other.height)
      cond3 = (self.width      == other.width)
      return True if cond1 and cond2 and cond3 else False

   def getItem(self, x, y):
      """ Return the specified gene of List

      Example:
         >>> genome.getItem(3, 1)
         0
      
      :param x: the x index, the column
      :param y: the y index, the row
      :rtype: the item at x,y position
      
      """
      return self.genomeString[x][y]

   def setItem(self, x, y, value):
      """ Set the specified gene of List

      Example:
         >>> genome.setItem(3, 1, 0)
      
      :param x: the x index, the column
      :param y: the y index, the row
      :param value: the value (integers 0 or 1)
      
      """
      if value not in [0,1]:
         Util.raiseException("The item value must be 0 or 1 in the G2DBinaryString chromosome", ValueError)
      self.genomeString[x][y] = value


   def __getitem__(self, key):
      """ Return the specified gene of List """
      return self.genomeString[key]

   def __iter__(self):
      """ Iterator support to the list """
      return iter(self.genomeString)
   
   def getHeight(self):
      """ Return the height (lines) of the List """
      return self.height

   def getWidth(self):
      """ Return the width (lines) of the List """
      return self.width

   def getSize(self):
      """ Returns a tuple (height, widht)
   
      Example:
         >>> genome.getSize()
         (3, 2)

      """
      return (self.getHeight(), self.getWidth())


   def __repr__(self):
      """ Return a string representation of Genome """
      ret = GenomeBase.__repr__(self)
      ret += "- G2DBinaryString\n"
      ret += "\tList size:\t %s\n" % (self.getSize(),)
      ret += "\tList:\n"
      for line in self.genomeString:
         ret += "\t\t\t"
         for item in line:
            ret += "[%s] " % (item)
         ret += "\n"
      ret += "\n"
      return ret

   def resumeString(self):
      """ Returns a resumed string representation of the Genome
      
      """
      ret = ""
      for line in self.genomeString:
         for item in line:
            ret += "[%s] " % (item)
         ret += "\n"
      return ret

   def clearString(self):
      """ Remove all genes from Genome """
      del self.genomeString[:]
      
      self.genomeString = [None]* self.height
      for i in xrange(self.height):
         self.genomeString[i] = [None] * self.width
   
   def copy(self, g):
      """ Copy genome to 'g'
      
      Example:
         >>> genome_origin.copy(genome_destination)
      
      :param g: the destination G2DBinaryString instance

      """
      GenomeBase.copy(self, g)
      g.height = self.height
      g.width = self.width
      for i in xrange(self.height):
         g.genomeString[i] = self.genomeString[i][:]
   
   def clone(self):
      """ Return a new instace copy of the genome
      
      :rtype: the G2DBinaryString clone instance

      """
      newcopy = G2DBinaryString(self.height, self.width)
      self.copy(newcopy)
      return newcopy

