from unittest import TestCase

from pyevolve import GSimpleGA, G1DList, Consts
from pyevolve.GTree import GTreeGP


class GSimpleGATestCase(TestCase):
    def setUp(self):
        self.genome = G1DList.G1DList(2)
        self.genome.evaluator.set(lambda _: 0)
        self.ga = GSimpleGA.GSimpleGA(self.genome)

    def test_works_fine(self):
        self.ga.evolve(freq_stats=1)
        self.assertTrue(self.ga.bestIndividual())

    def test_works_fine_with_elitism(self):
        self.ga.setElitismReplacement(2)
        self.ga.evolve(freq_stats=1)
        self.assertTrue(self.ga.bestIndividual())

    def test_get_different_results_for_different_evaluators(self):
        self.ga.evolve(freq_stats=1)
        result1 = self.ga.bestIndividual()
        self.genome.evaluator.set(lambda _: 100)
        self.ga = GSimpleGA.GSimpleGA(self.genome)
        self.ga.evolve(freq_stats=1)
        result2 = self.ga.bestIndividual()
        self.assertNotEquals(result1, result2)

    def test_fails_with_negative_evaluator(self):
        self.genome.evaluator.set(lambda _: -1)
        self.ga = GSimpleGA.GSimpleGA(self.genome)
        self.assertRaises(ValueError, self.ga.evolve, {'freq_stats': 1})

    def test_stem_call_replaces_internal_pop(self):
        self.ga.initialize()
        pop1 = self.ga.internalPop
        self.ga.step()
        pop2 = self.ga.internalPop
        self.assertFalse(pop1 is pop2)

    def test_gp_mode_is_set_for_tree_genome(self):
        ga = GSimpleGA.GSimpleGA(GTreeGP())
        self.assertTrue(ga.GPMode)

    def test_exception_on_wrong_multiprocessing_argument(self):
        self.assertRaises(TypeError, self.ga.setMultiProcessing, {'flag': 'not_bool_argument'})
        self.assertRaises(TypeError, self.ga.setMultiProcessing, {'full_copy': 'not_bool_argument'})
        self.assertRaises(TypeError, self.ga.setMultiProcessing, {'flag': 'not_bool_argument', 'full_copy': True})
        self.assertRaises(TypeError, self.ga.setMultiProcessing, {'flag': True, 'full_copy': 'not_bool_argument'})

    def test_exception_no_wrong_mutation_rate_size(self):
        self.assertRaises(ValueError, self.ga.setMutationRate, [2])

    def test_repr(self):
        ga = self.ga
        ga_repr = ga.__repr__()
        for param in [
            ga.getGPMode(),
            ga.internalPop.popSize,
            ga.nGenerations,
            ga.currentGeneration,
            ga.pMutation,
            ga.pCrossover,
            ga.elitism,
            ga.nElitismReplacement,
            ga.dbAdapter,
        ]:
            self.assertIn(str(param), ga_repr)