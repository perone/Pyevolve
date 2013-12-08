import unittest

from mock import patch

from pyevolve import Crossovers
from pyevolve.G1DBinaryString import G1DBinaryString


class CrossoverTestCase(unittest.TestCase):
    def assertCrossoverResultsEqual(self, crossover, expected_sister, expected_brother, crossover_extra_kwargs=None):
        crossover_extra_kwargs = crossover_extra_kwargs or {}
        kwargs = {
            'mom': self.mom,
            'dad': self.dad,
        }
        kwargs.update(crossover_extra_kwargs)
        actual_sister, actual_brother = [g.genomeList if g else None for g in crossover(None, **kwargs)]
        self.assertEqual(actual_sister, expected_sister)
        self.assertEqual(actual_brother, expected_brother)


class G1DBinaryStringCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G1DBinaryString(3)
        self.mom.append(1)
        self.mom.append(0)
        self.mom.append(0)
        self.dad = G1DBinaryString(3)
        self.dad.append(0)
        self.dad.append(0)
        self.dad.append(1)

    def test_x_single_point(self):
        self.assertCrossoverResultsEqual(
            Crossovers.G1DBinaryStringXSinglePoint,
            [1, 0, 1],
            [0, 0, 0],
            crossover_extra_kwargs={'count': 2}
        )

        self.assertCrossoverResultsEqual(
            Crossovers.G1DBinaryStringXSinglePoint,
            [1, 0, 1],
            None,
            crossover_extra_kwargs={'count': 1}
        )

    def test_x_two_point(self):
        self.assertCrossoverResultsEqual(
            Crossovers.G1DBinaryStringXTwoPoint,
            [1, 0, 0],
            [0, 0, 1],
            crossover_extra_kwargs={'count': 2}
        )

        self.assertCrossoverResultsEqual(
            Crossovers.G1DBinaryStringXTwoPoint,
            [1, 0, 0],
            None,
            crossover_extra_kwargs={'count': 1}
        )

    @patch('pyevolve.Util.randomFlipCoin')
    def test_x_uniform(self, coin_flip_mock):
        coin_flip_mock.return_value = [True, True, False]
        self.assertCrossoverResultsEqual(
            Crossovers.G1DBinaryStringXUniform,
            [0, 0, 1],
            [1, 0, 0],
        )
