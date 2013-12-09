import unittest

from mock import patch

from pyevolve.G1DBinaryString import G1DBinaryString
from pyevolve import Mutators, Consts
from pyevolve.G1DList import G1DList


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
