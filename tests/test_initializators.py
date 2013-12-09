import unittest

from pyevolve.G1DBinaryString import G1DBinaryString
from pyevolve import Initializators
from pyevolve.G1DList import G1DList
from pyevolve.G2DList import G2DList
from pyevolve.GTree import GTree


class InitializatorsTestCase(unittest.TestCase):
    def test_binary_string_initializator(self):
        genome = G1DBinaryString(3)
        Initializators.G1DBinaryStringInitializator(genome)
        for gen in genome.genomeList:
            self.assertTrue(gen in [0, 1])

    def test_1d_list_real_initializator(self):
        genome = G1DList(3)
        Initializators.G1DListInitializatorReal(genome)
        for gen in genome.genomeList:
            self.assertTrue(type(gen) == float)

    def test_2d_list_integer_initializator(self):
        genome = G2DList(3, 3)
        Initializators.G2DListInitializatorInteger(genome)
        for gen_row in genome.genomeList:
            for gen in gen_row:
                self.assertTrue(type(gen) == int)

    def test_2d_list_real_initializator(self):
        genome = G2DList(3, 3)
        Initializators.G2DListInitializatorReal(genome)
        for gen_row in genome.genomeList:
            for gen in gen_row:
                self.assertTrue(type(gen) == float)

    def test_tree_integer_initializator(self):
        genome = GTree()
        genome.setParams(max_depth=3)
        Initializators.GTreeInitializatorInteger(genome)
        for gen in genome.getAllNodes():
            self.assertTrue(type(gen.getData()) == int)
