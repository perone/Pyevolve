"""

:mod:`G1DList` -- the 1D list chromosome
=============================================================

This is the 1D List representation, this list can carry real
numbers or integers or any kind of object, by default, we have
genetic operators for integer and real lists, which can be found
on the respective modules.

Default Parameters
-------------------------------------------------------------

*Initializator*

   :func:`Initializators.G1DListInitializatorInteger`

   The Integer Initializator for G1DList

*Mutator*

   :func:`Mutators.G1DListMutatorSwap`

   The Swap Mutator for G1DList

*Crossover*

   :func:`Crossovers.G1DListCrossoverSinglePoint`

   The Single Point Crossover for G1DList


Class
-------------------------------------------------------------

"""
from GenomeBase import GenomeBase, G1DBase
import Consts


class G1DList(G1DBase):
    """ G1DList Class - The 1D List chromosome representation

    Inheritance diagram for :class:`G1DList.G1DList`:

    .. inheritance-diagram:: G1DList.G1DList

    This chromosome class extends the :class:`GenomeBase.GenomeBase` class.

    **Examples**

       The instantiation
          >>> g = G1DList(10)

       Compare
          >>> genome2 = genome1.clone()
          >>> genome2 == genome1
          True

       Multiply
          >>> genome = population[0]
          >>> genome
          (...)
          [1, 2, 3, 4]
          >>> genome_result = genome * 2
          >>> genome_result
          (...)
          [2, 2, 6, 8]

       Add
          >>> genome
          (...)
          [1, 2, 3, 4]
          >>> genome_result = genome + 2
          (...)
          [3, 4, 5, 6]

       Iteration
          >>> for i in genome:
          >>>   print i
          1
          2
          3
          4

       Size, slice, get/set, append
          >>> len(genome)
          4
          >>> genome
          (...)
          [1, 2, 3, 4]
          >>> genome[0:1]
          [1, 2]
          >>> genome[1] = 666
          >>> genome
          (...)
          [1, 666, 3, 4]
          >>> genome.append(99)
          >>> genome
          (...)
          [1, 666, 3, 4, 99]

    :param size: the 1D list size

    """

    def __init__(self, size=10, cloning=False):
        """ The initializator of G1DList representation,
        size parameter must be specified """
        super(G1DList, self).__init__(size)
        if not cloning:
            self.initializator.set(Consts.CDefG1DListInit)
            self.mutator.set(Consts.CDefG1DListMutator)
            self.crossover.set(Consts.CDefG1DListCrossover)

    def __mul__(self, other):
        """ Multiply every element of G1DList by "other" """
        newObj = self.clone()
        for i in xrange(len(newObj)):
            newObj[i] *= other
        return newObj

    def __add__(self, other):
        """ Plus every element of G1DList by "other" """
        newObj = self.clone()
        for i in xrange(len(newObj)):
            newObj[i] += other
        return newObj

    def __sub__(self, other):
        """ Plus every element of G1DList by "other" """
        newObj = self.clone()
        for i in xrange(len(newObj)):
            newObj[i] -= other
        return newObj

    def __repr__(self):
        """ Return a string representation of Genome """
        ret = GenomeBase.__repr__(self)
        ret += "- G1DList\n"
        ret += "\tList size:\t %s\n" % (self.getListSize(),)
        ret += "\tList:\t\t %s\n\n" % (self.genomeList,)
        return ret

    def copy(self, g):
        """ Copy genome to 'g'

        Example:
           >>> genome_origin.copy(genome_destination)

        :param g: the destination G1DList instance

        """
        GenomeBase.copy(self, g)
        G1DBase.copy(self, g)

    def clone(self):
        """ Return a new instace copy of the genome

        :rtype: the G1DList clone instance

        """
        newcopy = G1DList(self.genomeSize, True)
        self.copy(newcopy)
        return newcopy
