from unittest import TestCase

from pyevolve import GSimpleGA, G1DList
from pyevolve.GTree import GTreeGP


class GSimpleGATestCase(TestCase):
    def setUp(self):
        genome = G1DList.G1DList(2)
        genome.evaluator.set(lambda _: 0)
        self.ga = GSimpleGA.GSimpleGA(genome)

    def test_works_fine(self):
        self.ga.evolve(freq_stats=1)
        self.assertTrue(self.ga.bestIndividual())

    def test_gp_mode_is_set_for_tree_genome(self):
        ga = GSimpleGA.GSimpleGA(GTreeGP())
        self.assertTrue(ga.GPMode)

    def test_exception_on_wrong_multiprocessing_argument(self):
        self.assertRaises(TypeError, self.ga.setMultiProcessing, {'flag': 'not_bool_argument'})
        self.assertRaises(TypeError, self.ga.setMultiProcessing, {'full_copy': 'not_bool_argument'})
