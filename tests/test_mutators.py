import unittest

from mock import patch, Mock

from pyevolve.G1DBinaryString import G1DBinaryString
from pyevolve import Mutators, Consts
from pyevolve.G1DList import G1DList
from pyevolve.G2DCartesian import G2DCartesian, CartesianNode
from random import randint


class G1DBinaryStringMutatorsTestCase(unittest.TestCase):
    def setUp(self):
        self.genome = G1DBinaryString(3)
        self.genome.append(1)
        self.genome.append(0)
        self.genome.append(0)

    @patch('pyevolve.Util.randomFlipCoin')
    def test_swap_mutator_small_pmut(self, coin_flip_mock):
        coin_flip_mock.return_value = 0
        expected_result = [1, 0, 0]
        Mutators.G1DBinaryStringMutatorSwap(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    def test_swap_mutator_large_pmut(self, rand_mock):
        rand_mock.return_value = 0
        expected_result = [1, 0, 0]
        Mutators.G1DBinaryStringMutatorSwap(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)


    @patch('pyevolve.Util.randomFlipCoin')
    def test_flip_mutator_small_pmut(self, coin_flip_mock):
        coin_flip_mock.return_value = 1
        expected_result = [0, 1, 1]
        Mutators.G1DBinaryStringMutatorFlip(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    def test_flip_mutator_large_pmut(self, rand_mock):
        rand_mock.return_value = 0
        expected_result = [1, 0, 0]
        Mutators.G1DBinaryStringMutatorFlip(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)


class G1DListMutatorsTestCase(unittest.TestCase):
    def setUp(self):
        self.genome = G1DList(3)
        self.genome.genomeList = [1, 2, 3]

    @patch('pyevolve.Util.randomFlipCoin')
    @patch('pyevolve.Mutators.rand_randint')
    def test_sim_mutator(self, rand_mock, coin_flip_mock):
        rand_mock.side_effect = [0, 2]
        coin_flip_mock.return_value = 1
        expected_result = [2, 1, 3]
        Mutators.G1DListMutatorSIM(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Util.randomFlipCoin')
    @patch('pyevolve.Mutators.rand_randint')
    def test_range_mutator_small_pmut(self, rand_mock, coin_flip_mock):
        coin_flip_mock.return_value = 1
        rand_mock.side_effect = [0, 2, 4]
        expected_result = [0, 2, 4]
        Mutators.G1DListMutatorIntegerRange(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    def test_range_mutator_large_pmut(self, rand_mock):
        rand_mock.return_value = 0
        expected_result = [0, 2, 3]
        Mutators.G1DListMutatorIntegerRange(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Util.randomFlipCoin')
    @patch('pyevolve.Mutators.rand_uniform')
    def test_real_range_mutator_small_pmut(self, rand_mock, coin_flip_mock):
        coin_flip_mock.return_value = 1
        rand_mock.side_effect = [0, 2, 4]
        expected_result = [0, 2, 4]
        Mutators.G1DListMutatorRealRange(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    @patch('pyevolve.Mutators.rand_uniform')
    def test_real_range_mutator_large_pmut(self, rand_uniform_mock, rand_mock):
        rand_mock.return_value = 0
        rand_uniform_mock.return_value = Consts.CDefRangeMin
        expected_result = [0, 2, 3]
        Mutators.G1DListMutatorRealRange(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Util.randomFlipCoin')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_integer_gauss_grad_mutator_small_pmut(self, rand_mock, coin_flip_mock):
        coin_flip_mock.return_value = 1
        rand_mock.side_effect = [0, 2, 4]
        expected_result = [0, 4, 12]
        Mutators.G1DListMutatorIntegerGaussianGradient(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_integer_gauss_grad_mutator_large_pmut(self, rand_gauss_mock, rand_mock):
        rand_mock.return_value = 0
        rand_gauss_mock.return_value = Consts.CDefRangeMin
        expected_result = [0, 2, 3]
        Mutators.G1DListMutatorIntegerGaussianGradient(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Util.randomFlipCoin')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_integer_gauss_mutator_small_pmut(self, rand_mock, coin_flip_mock):
        coin_flip_mock.return_value = 1
        rand_mock.side_effect = [0, 2, 4]
        expected_result = [1, 4, 7]
        Mutators.G1DListMutatorIntegerGaussian(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_integer_gauss_mutator_large_pmut(self, rand_gauss_mock, rand_mock):
        rand_mock.return_value = 0
        rand_gauss_mock.return_value = Consts.CDefRangeMin
        expected_result = [1, 2, 3]
        Mutators.G1DListMutatorRealGaussian(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Util.randomFlipCoin')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_real_gauss_mutator_small_pmut(self, rand_mock, coin_flip_mock):
        coin_flip_mock.return_value = 1
        rand_mock.side_effect = [0, 2, 4]
        expected_result = [1, 4, 7]
        Mutators.G1DListMutatorRealGaussian(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_real_gauss_mutator_large_pmut(self, rand_gauss_mock, rand_mock):
        rand_mock.return_value = 0
        rand_gauss_mock.return_value = Consts.CDefRangeMin
        expected_result = [1, 2, 3]
        Mutators.G1DListMutatorRealGaussian(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Util.randomFlipCoin')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_real_gauss_grad_mutator_small_pmut(self, rand_mock, coin_flip_mock):
        coin_flip_mock.return_value = 1
        rand_mock.side_effect = [0, 2, 4]
        expected_result = [0, 4, 12]
        Mutators.G1DListMutatorRealGaussianGradient(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    @patch('pyevolve.Mutators.rand_gauss')
    def test_real_gauss_grad_mutator_large_pmut(self, rand_gauss_mock, rand_mock):
        rand_mock.return_value = 0
        rand_gauss_mock.return_value = Consts.CDefRangeMin
        expected_result = [0, 2, 3]
        Mutators.G1DListMutatorRealGaussianGradient(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Util.randomFlipCoin')
    def test_binary_mutator_small_pmut(self, coin_flip_mock):
        coin_flip_mock.return_value = 1
        expected_result = [0, 2, 3]
        Mutators.G1DListMutatorIntegerBinary(self.genome, pmut=0.1)
        self.assertEqual(self.genome.genomeList, expected_result)

    @patch('pyevolve.Mutators.rand_randint')
    def test_binary_mutator_large_pmut(self, rand_mock):
        rand_mock.return_value = 0
        expected_result = [1, 2, 3]
        Mutators.G1DListMutatorIntegerBinary(self.genome, pmut=0.5)
        self.assertEqual(self.genome.genomeList, expected_result)

class G2DCartesianMutatorsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        CartesianNode.paramMapping.clear()

    def setUp(self):
        self.function_set = {'f1' : 2, 'f3' : 3, 'f4' : 5}
        self.genome = G2DCartesian(2, 2, 1, 1)
        
        self.genome[0] = CartesianNode(0, -1, {'a' : 1}, [])
        prevs = [self.genome[0]]
        self.genome[1] = CartesianNode(0, 0, {'f1' : 2}, prevs)    
        self.genome[2] = CartesianNode(1, 0, {'f2' : 2}, prevs)
        prevs.append(self.genome[1])
        prevs.append(self.genome[2])
        self.genome[3] = CartesianNode(0, 1, {'f3' : 3}, prevs)
        self.genome[4] = CartesianNode(1, 1, {'f4' : 3}, prevs)
        prevs.append(self.genome[3])
        prevs.append(self.genome[4])
        self.genome[5] = CartesianNode(0, 2, {}, prevs)
        
        def side_param(arg):
            if arg == "gp_function_set":
                return self.function_set
        
        self.ga_engine = Mock()        
        self.ga_engine.getParam = side_param                

    @patch('pyevolve.Mutators.rand_choice')
    def test_cartesian_mutator_inputs_small_pmut(self, rand_mock):
        expected_result = []
        values = [3, 0, 2]                        
        def choice_effect(arg):                                          
            return self.genome[values.pop(0)]
    
        rand_mock.side_effect = choice_effect
        
        for i in values[1:]:
            expected_result.append(self.genome[i])
        Mutators.G2DCartesianMutatorNodeInputs(self.genome, pmut=0.1)
        self.assertEqual(self.genome[3].inputs, expected_result)
        
    @patch('pyevolve.Mutators.rand_choice')
    def test_cartesian_mutator_inputs_large_pmut(self, rand_mock):
        expected_result = {}
        values = [1, 0, 2, 0 , 3, 1, 0, 4, 1, 2]        
        def choice_effect(arg):                                          
            return self.genome[values.pop(0)]
                    
        rand_mock.side_effect = choice_effect
        
        idx = 0
        while idx < len(values):
            expected_result[values[idx]] = []
            node_idx = idx
            for input in self.genome[values[idx]].inputs:
                idx = idx+1
                expected_result[values[node_idx]].append(
                                                    self.genome[values[idx]])
            idx = idx+1
        
        Mutators.G2DCartesianMutatorNodeInputs(self.genome, pmut=0.7)        
        for key in expected_result.keys():
            self.assertEqual(self.genome[key].inputs, expected_result[key])
     
    @patch('pyevolve.Mutators.rand_choice')
    def test_cartesian_mutator_function_small_pmut(self, rand_mock):        
        values = [4, "f3"]        
        def choice_effect(arg):
            what = values.pop(0)
            if isinstance(what, int):            
                return self.genome[what]
            else:
                return what
                    
        rand_mock.side_effect = choice_effect                
        Mutators.G2DCartesianMutatorNodeFunction(self.genome, pmut=0.1, 
                                                    ga_engine = self.ga_engine)        
        self.assertEqual(self.genome[4].data, "f3")
        self.assertEqual(len(self.genome[4].inputs), self.function_set["f3"]-1)
        
    @patch('pyevolve.Mutators.rand_choice')
    def test_cartesian_mutator_function_large_pmut(self, rand_mock):
        values = [1, "f3", 0,  2, "f4", 0, 0, 0, 3, "f1", 4, "f4", 0, 0]
        def choice_effect(arg):
            what = values.pop(0)
            if isinstance(what, int):            
                return self.genome[what]
            else:
                return what
                    
        rand_mock.side_effect = choice_effect                
        Mutators.G2DCartesianMutatorNodeFunction(self.genome, pmut=0.7, 
                                                    ga_engine = self.ga_engine)
        values = [1, "f3", 0,  2, "f4", 0, 0, 0, 3, "f1", 4, "f4", 0, 0]                 
        idx = 0
        while idx >= 0:
            values = values[idx:]
            node_idx = values[0]
            func = values[1]
            self.assertEqual(self.genome[node_idx].data, func)
            self.assertEqual(len(self.genome[node_idx].inputs), 
                                self.function_set[func]-1)
            values = values[2:]
            idx = (next((key for key, val in 
                                enumerate(values) if 
                                        isinstance(val, str)), 0) - 1)                
     
    @patch('pyevolve.Mutators.rand_choice')
    def test_cartesian_mutator_params_small_pmut(self, rand_mock):
        CartesianNode.paramMapping = {"p1" : "rand_randint(0,10)",
                                        "p2" : "rand_randint(0,10)"}
        value = 3
        for param in CartesianNode.paramMapping.keys():
            self.genome[value].params[param] = -1
        rand_mock.return_value = self.genome[value]
        Mutators.G2DCartesianMutatorNodeParams(self.genome, pmut=0.1)
        for param in self.genome[value].params.values():
            self.assertTrue(param in range(0,11))
        CartesianNode.paramMapping.clear()
        
    @patch('pyevolve.Mutators.rand_choice')
    def test_cartesian_mutator_params_large_pmut(self, rand_mock):
        CartesianNode.paramMapping = {"p1" : "rand_randint(0,10)",
                                        "p2" : "rand_randint(0,10)"}
        values = [1, 2, 3, 4]
        for v in values:
            for param in CartesianNode.paramMapping.keys():
                self.genome[v].params[param] = -1
        def choice_effect(arg):
            return self.genome[values.pop(0)]
        rand_mock.side_effect = choice_effect
        Mutators.G2DCartesianMutatorNodeParams(self.genome, pmut=0.7)
        values = [1, 2, 3, 4]
        for v in values:
            for param in self.genome[v].params.values():
                self.assertTrue(param in range(0,11))
        CartesianNode.paramMapping.clear()
        
    @patch('pyevolve.Mutators.rand_shuffle')
    def test_cartesian_mutator_order(self, rand_mock):
        self.genome[5].inputs = [self.genome[4]]
        self.genome[4].inputs = [self.genome[1]]
        self.genome[1].inputs = [self.genome[0]]

        expected_order = [("f4", 5), ("f3", 1)]
        def shuffle_effect(arg):            
            arg[:] = list(expected_order)
            return
            
        rand_mock.side_effect = shuffle_effect
        Mutators.G2DCartesianMutatorNodesOrder(self.genome, pmut=0.2)        
        paths = self.genome.getActiveNodes()            
        shuffled_functions = []
        for node in paths[0]:
            shuffled_functions.append(node.getData())

        for func in expected_order:
            self.assertTrue(func in shuffled_functions)