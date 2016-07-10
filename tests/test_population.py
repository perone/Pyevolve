from unittest import TestCase
from mock import MagicMock
from pyevolve.GPopulation import GPopulation


class MultithreadingTestCase(TestCase):
    def setUp(self):
        
        self.scores = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]
        def eval_effect(idx):            
            self.population.internalPop[idx].score = self.scores[idx]
        
        self.mockGenome = MagicMock()
        self.population = GPopulation(self.mockGenome)        
        self.population.internalPop = [MagicMock() for _ in xrange(0,11)]        
        for idx, mock in enumerate(self.population.internalPop):
            mock.score = 0.0
            mock.evaluate = MagicMock(side_effect = eval_effect(idx))             
        
    def test_init(self):
        self.assertTrue(self.population.multiThreading == (False, None))
        
    def test_set_MT(self):
        self.population.setMultiThreading(True, 10)
        self.assertTrue(self.population.multiThreading == (True, 10))
        
    def test_run_MT_without_constraint(self):
        self.population.setMultiThreading(True)
        self.population.evaluate()
        for ind in self.population.internalPop:
            self.assertTrue(ind.score in self.scores)
            
    def test_run_MT_with_constraints(self):
        self.population.setMultiThreading(True, 3)
        self.population.evaluate()
        for ind in self.population.internalPop:
            self.assertTrue(ind.score in self.scores)