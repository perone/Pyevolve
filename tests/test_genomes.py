# flake8: noqa
from collections import Iterable
from unittest import TestCase

from pyevolve import G1DBinaryString
from pyevolve import G1DList
from pyevolve import G2DBinaryString
from pyevolve import G2DList
from pyevolve.GenomeBase import G1DBase
from pyevolve.GenomeBase import GTreeBase
from pyevolve.GTree import GTree
from pyevolve.GTree import GTreeNode
from pyevolve.GTree import GTreeNodeBase
from pyevolve.GTree import GTreeNodeGP


class G1DBinaryStringTestCase(TestCase):

    # def setUp(self):
    #     self._stats = Statistics.Statistics()

    def test_create1DBinary_default(self):
        _genome = G1DBinaryString.G1DBinaryString()
        self.assertTrue(hasattr(_genome, 'genomeList'))
        self.assertTrue(hasattr(_genome, 'genomeSize'))
        self.assertIsInstance(_genome.genomeSize, int)
        self.assertTrue(hasattr(_genome, 'initializator'))
        self.assertTrue(hasattr(_genome, 'mutator'))
        self.assertTrue(hasattr(_genome, 'crossover'))

    def test_create1DBinary_len(self):
        _genome = G1DBinaryString.G1DBinaryString(length=5)
        self.assertTrue(hasattr(_genome, 'genomeList'))
        self.assertEqual(_genome.genomeSize, 5)
        self.assertTrue(hasattr(_genome, 'initializator'))
        self.assertTrue(hasattr(_genome, 'mutator'))
        self.assertTrue(hasattr(_genome, 'crossover'))

    def test_1DBinarySetitem(self):
        _genome = G1DBinaryString.G1DBinaryString(length=5)
        _genome.append(0)
        _genome.append(1)
        _genome.append(1)
        self.assertEqual(_genome[0], 0)
        with self.assertRaises(ValueError):
            _genome[0] = 2
        with self.assertRaises(ValueError):
            _genome[0:2] = [0,1,2]

    def test_getBinary(self):
        _genome = G1DBinaryString.G1DBinaryString()
        self.assertIsInstance(_genome.getBinary(), str)

    def test_getDecimal(self):
        _genome = G1DBinaryString.G1DBinaryString(length=3)
        _genome.append(0)
        _genome.append(1)
        _genome.append(1)
        self.assertEqual(_genome.getDecimal(), 3)

    def test_append(self):
        _genome = G1DBinaryString.G1DBinaryString(length=3)
        _genome.append(0)
        _genome.append(1)
        self.assertEqual(_genome[0], 0)
        with self.assertRaises(ValueError):
            _genome.append(2)

    def test_repr(self):
        _genome = G1DBinaryString.G1DBinaryString()
        self.assertIsInstance(repr(_genome), str)


class G2DListTestCase(TestCase):

    # def setUp(self):
    #     self._stats = Statistics.Statistics()

    def test_create2DList_default(self):
        _genome = G2DList.G2DList(3, 3)
        self.assertTrue(hasattr(_genome, 'width'))
        self.assertTrue(hasattr(_genome, 'height'))
        self.assertTrue(hasattr(_genome, 'genomeList'))
        self.assertTrue(hasattr(_genome, 'initializator'))
        self.assertTrue(hasattr(_genome, 'mutator'))
        self.assertTrue(hasattr(_genome, 'crossover'))

    def test_2DList_eq(self):
        _genome1 = G2DList.G2DList(3, 2)
        _genome2 = G2DList.G2DList(3, 3)
        self.assertFalse(_genome1 == _genome2)

        _genome1 = G2DList.G2DList(2, 3)
        _genome2 = G2DList.G2DList(3, 3)
        self.assertFalse(_genome1 == _genome2)

        _genome1 = G2DList.G2DList(3, 3)
        _genome2 = G2DList.G2DList(3, 3)
        _genome1.setItem(2, 1, 0)
        _genome2.setItem(2, 1, 1)
        self.assertFalse(_genome1 == _genome2)

        _genome1 = G2DList.G2DList(3, 3)
        _genome2 = G2DList.G2DList(3, 3)
        self.assertTrue(_genome1 == _genome2)

    def test_2DList_iter(self):
        _genome = G2DList.G2DList(3, 3)
        self.assertIsInstance(iter(_genome), Iterable)

    def test_repr(self):
        _genome = G2DList.G2DList(3, 3)
        self.assertIsInstance(repr(_genome), str)

    def test_2DList_resumeString(self):
        _genome = G2DList.G2DList(3, 3)
        self.assertIsInstance(_genome.resumeString(), str)


class G1DListTestCase(TestCase):

    # def setUp(self):
    #     self._stats = Statistics.Statistics()

    def test_create1DList_default(self):
        _genome = G1DList.G1DList()
        self.assertTrue(hasattr(_genome, 'genomeSize'))
        self.assertTrue(hasattr(_genome, 'initializator'))
        self.assertTrue(hasattr(_genome, 'mutator'))
        self.assertTrue(hasattr(_genome, 'crossover'))

    def test_1DList_mul(self):
        _genome1 = G1DList.G1DList(size=3)
        _genome1[:] = [1, 2, 3]
        other = 2
        result = _genome1 * other
        self.assertEqual(result.genomeList, [2, 4, 6])

    def test_1DList_add(self):
        _genome1 = G1DList.G1DList(size=3)
        _genome1[:] = [1, 2, 3]
        other = 2
        result = _genome1 + other
        self.assertEqual(result.genomeList, [3, 4, 5])

    def test_1DList_sub(self):
        _genome1 = G1DList.G1DList(size=3)
        _genome1[:] = [1, 2, 3]
        other = 2
        result = _genome1 - other
        self.assertEqual(result.genomeList, [-1, 0, 1])

    def test_repr(self):
        _genome = G1DList.G1DList()
        self.assertIsInstance(repr(_genome), str)


class G2DBinaryStringTestCase(TestCase):

    # def setUp(self):
    #     self._stats = Statistics.Statistics()

    def test_create2DBinary_default(self):
        _genome = G2DBinaryString.G2DBinaryString(3, 3)
        self.assertTrue(hasattr(_genome, 'width'))
        self.assertTrue(hasattr(_genome, 'height'))
        self.assertTrue(hasattr(_genome, 'initializator'))
        self.assertTrue(hasattr(_genome, 'mutator'))
        self.assertTrue(hasattr(_genome, 'crossover'))

    def test_2DBinary_eq(self):
        _genome1 = G2DBinaryString.G2DBinaryString(3, 2)
        _genome2 = G2DBinaryString.G2DBinaryString(3, 3)
        self.assertFalse(_genome1 == _genome2)

        _genome1 = G2DBinaryString.G2DBinaryString(2, 3)
        _genome2 = G2DBinaryString.G2DBinaryString(3, 3)
        self.assertFalse(_genome1 == _genome2)

        _genome1 = G2DBinaryString.G2DBinaryString(3, 3)
        _genome2 = G2DBinaryString.G2DBinaryString(3, 3)
        _genome1.setItem(2, 1, 0)
        _genome2.setItem(2, 1, 1)
        self.assertFalse(_genome1 == _genome2)

        _genome1 = G2DBinaryString.G2DBinaryString(3, 3)
        _genome2 = G2DBinaryString.G2DBinaryString(3, 3)
        self.assertTrue(_genome1 == _genome2)

    def test_2DBinary_setitem(self):
        _genome = G2DBinaryString.G2DBinaryString(3, 3)
        _genome.setItem(1,1,1)
        self.assertEqual(_genome.getItem(1,1), 1)
        with self.assertRaises(ValueError):
            _genome.setItem(1, 1, 2)


    def test_2DBinary_iter(self):
        _genome = G2DBinaryString.G2DBinaryString(3, 3)
        self.assertIsInstance(iter(_genome), Iterable)

    def test_repr(self):
        _genome = G2DBinaryString.G2DBinaryString(3, 3)
        self.assertIsInstance(repr(_genome), str)

    def test_2DBinary_resumeString(self):
        _genome = G2DBinaryString.G2DBinaryString(3, 3)
        self.assertIsInstance(_genome.resumeString(), str)

    def test_2DBinary_clearString(self):
        _genome = G2DBinaryString.G2DBinaryString(2, 4)
        _genome.clearString()
        self.assertEqual(len(_genome.genomeString), _genome.getHeight())
        self.assertEqual(len(_genome.genomeString[0]), _genome.getWidth())
        self.assertEqual(_genome[1][1], None)