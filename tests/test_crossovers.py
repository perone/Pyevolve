from itertools import cycle
import unittest

from mock import patch
from nose.tools import nottest

from pyevolve import Crossovers
from pyevolve.G1DBinaryString import G1DBinaryString
from pyevolve.G1DList import G1DList
from pyevolve.G2DBinaryString import G2DBinaryString
from pyevolve.G2DList import G2DList
from pyevolve.GTree import GTree, GTreeNode


class CrossoverTestCase(unittest.TestCase):
    def assertCrossoverResultsEqual(
            self,
            crossover,
            expected_sister,
            expected_brother,
            crossover_extra_kwargs=None,
            genome_attr_name='genomeList',  # TODO refactor with Genome getter method
            assertion_name='assertEqual'
    ):
        crossover_extra_kwargs = crossover_extra_kwargs or {}
        kwargs = {
            'mom': self.mom,
            'dad': self.dad,
        }
        kwargs.update(crossover_extra_kwargs)
        genome_value_getter = lambda g: getattr(g, genome_attr_name) if genome_attr_name else g
        actual_sister, actual_brother = [genome_value_getter(g) if g else None for g in crossover(None, **kwargs)]
        getattr(self, assertion_name)(actual_sister, expected_sister)
        getattr(self, assertion_name)(actual_brother, expected_brother)


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

    @patch('pyevolve.Crossovers.rand_randint')
    def test_single_point(self, rand_mock):
        rand_mock.return_value = 1
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

    @patch('pyevolve.Crossovers.rand_randint')
    def test_two_point(self, rand_mock):
        rand_mock.return_value = 1
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
    def test_uniform(self, coin_flip_mock):
        coin_flip_mock.return_value = [1, 1, 0]
        self.assertCrossoverResultsEqual(
            Crossovers.G1DBinaryStringXUniform,
            [0, 0, 1],
            [1, 0, 0],
        )


class G1DListCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G1DList(3)
        self.mom.genomeList = [1, 2, 3]
        self.dad = G1DList(3)
        self.dad.genomeList = [4, 5, 6]

    @patch('pyevolve.Crossovers.rand_randint')
    def test_single_point(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverSinglePoint,
            [1, 5, 6],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverSinglePoint,
            [1, 5, 6],
            [4, 2, 3],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Crossovers.rand_randint')
    def test_two_points(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverTwoPoint,
            [1, 2, 3],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverTwoPoint,
            [1, 2, 3],
            [4, 5, 6],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Util.randomFlipCoin')
    def test_uniform(self, coin_flip_mock):
        coin_flip_mock.return_value = [1, 0, 0]
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverUniform,
            [4, 5, 6],
            [1, 2, 3],
        )

    @nottest  # fails because of https://github.com/perone/Pyevolve/issues/26
    @patch('pyevolve.Crossovers.rand_randint')
    def test_order_crossover(self, rand_mock):
        rand_mock.side_effect = [1, 2]
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverOX,
            [1, 2, 3],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverOX,
            [1, 2, 3],
            [4, 5, 6],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Crossovers.rand_randint')
    def test_crossfill_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverCutCrossfill,
            [1, 4, 5],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverCutCrossfill,
            [1, 4, 5],
            [4, 1, 2],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Crossovers.rand_random')
    def test_crossfill_crossover(self, rand_mock):
        rand_mock.return_value = 0.6
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverRealSBX,
            [0.9696386870268516, 1.9692699516972016, 2.9692611909097177],
            [4.030739398252697, 5.030739398252697, 6.030739398252697],
        )

    @patch('pyevolve.Crossovers.rand_randint')
    def test_crossfill_cut_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverCutCrossfill,
            [1, 4, 5],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverCutCrossfill,
            [1, 4, 5],
            [4, 1, 2],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Crossovers.rand_choice')
    def test_edge_crossover(self, rand_mock):
        rand_mock.side_effect = lambda u: u[0]
        self.assertCrossoverResultsEqual(
            Crossovers.G1DListCrossoverEdge,
            [1, 2, 3],
            [4, 5, 6],
        )


class G2DListCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G2DList(3, 3)
        self.mom.genomeList = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.dad = G2DList(3, 3)
        self.dad.genomeList = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    @patch('pyevolve.Util.randomFlipCoin')
    def test_uniform_crossover(self, coin_flip_mock):
        coin_flip_mock.return_value = cycle([1, 0, 0])
        self.assertCrossoverResultsEqual(
            Crossovers.G2DListCrossoverUniform,
            [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        )

    @patch('pyevolve.Crossovers.rand_randint')
    def test_svp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G2DListCrossoverSingleVPoint,
            [[1, 4, 7], [4, 5, 8], [7, 6, 9]],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G2DListCrossoverSingleVPoint,
            [[1, 4, 7], [4, 5, 8], [7, 6, 9]],
            [[1, 2, 3], [2, 5, 6], [3, 8, 9]],
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Crossovers.rand_randint')
    def test_shp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G2DListCrossoverSingleHPoint,
            [[1, 2, 3], [2, 5, 8], [3, 6, 9]],
            None,
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G2DListCrossoverSingleHPoint,
            [[1, 2, 3], [2, 5, 8], [3, 6, 9]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            crossover_extra_kwargs={'count': 2}
        )


class G2DBinaryStringCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        self.mom = G2DBinaryString(3, 3)
        self.mom.genomeString = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
        self.dad = G2DBinaryString(3, 3)
        self.dad.genomeString = [[0, 1, 1], [1, 0, 0], [1, 0, 1]]

    @patch('pyevolve.Util.randomFlipCoin')
    def test_uniform_crossover(self, coin_flip_mock):
        coin_flip_mock.return_value = cycle([1, 0, 0])
        self.assertCrossoverResultsEqual(
            Crossovers.G2DBinaryStringXUniform,
            [[0, 1, 1], [1, 0, 0], [1, 0, 1]],
            [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
            genome_attr_name='genomeString'
        )

    @patch('pyevolve.Crossovers.rand_randint')
    def test_svp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G2DBinaryStringXSingleVPoint,
            [[0, 1, 1], [0, 0, 0], [0, 0, 1]],
            None,
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G2DBinaryStringXSingleVPoint,
            [[0, 1, 1], [0, 0, 0], [0, 0, 1]],
            [[0, 0, 0], [1, 0, 1], [1, 1, 0]],
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 2}
        )

    @patch('pyevolve.Crossovers.rand_randint')
    def test_shp_crossover(self, rand_mock):
        rand_mock.return_value = 1
        self.assertCrossoverResultsEqual(
            Crossovers.G2DBinaryStringXSingleHPoint,
            [[0, 0, 0], [1, 0, 0], [1, 0, 1]],
            None,
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.G2DBinaryStringXSingleHPoint,
            [[0, 0, 0], [1, 0, 0], [1, 0, 1]],
            [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
            genome_attr_name='genomeString',
            crossover_extra_kwargs={'count': 2}
        )


class GTreeCrossoversTestCase(CrossoverTestCase):
    def setUp(self):
        mom_root = GTreeNode(1)
        mom_root.addChild(GTreeNode(2))
        mom_root.addChild(GTreeNode(3))
        self.mom = GTree(mom_root)
        self.mom.setParams(max_depth=2)
        dad_root = GTreeNode(4)
        dad_root.addChild(GTreeNode(5))
        dad_root.addChild(GTreeNode(6))
        self.dad = GTree(dad_root)
        self.dad.setParams(max_depth=2)

    def assetTreesEqual(self, tree1, tree2):
        """ Compares values of simplest trees with root and leafes from root"""
        self.assertFalse((tree1 is None and tree2 is not None) or (tree1 is not None and tree2 is None))
        if not(tree1 is None and tree2 is None):
            root1, root2 = tree1.getRoot(), tree2.getRoot()
            self.assertEqual(root1.node_data, root2.node_data)
            root1_childs = set([l.node_data for l in root1.getChilds()])
            root2_childs = set([l.node_data for l in root2.getChilds()])
            print root1_childs, root2_childs
            self.assertFalse((root1_childs and not root2_childs) or (not root1_childs and root2_childs))
            print root1_childs, root2_childs
            self.assertFalse(root1_childs - root2_childs)

    @patch('pyevolve.Crossovers.rand_choice')
    def test_single_point_crossover(self, rand_mock):
        rand_mock.side_effect = lambda u: u[0]

        expected_root1 = GTreeNode(1)  # TODO refactor after <BUG URL HERE>
        expected_root1.addChild(GTreeNode(2))
        expected_root1.addChild(GTreeNode(6))
        expected_root2 = GTreeNode(4)
        expected_root2.addChild(GTreeNode(3))
        expected_root2.addChild(GTreeNode(5))

        self.assertCrossoverResultsEqual(
            Crossovers.GTreeCrossoverSinglePoint,
            GTree(expected_root1),
            None,
            genome_attr_name=None,
            assertion_name='assetTreesEqual',
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.GTreeCrossoverSinglePoint,
            GTree(expected_root1),
            GTree(expected_root2),
            genome_attr_name=None,
            assertion_name='assetTreesEqual',
            crossover_extra_kwargs={'count': 2}
        )

    @nottest  # patch GTreeBase.getRandomNode
    @patch('pyevolve.Crossovers.rand_choice')
    def test_strict_single_point_crossover(self, rand_mock):
        rand_mock.side_effect = lambda u: u[0]

        expected_root1 = GTreeNode(6)  # TODO refactor after <BUG URL HERE>
        expected_root1.addChild(GTreeNode(2))
        expected_root1.addChild(GTreeNode(6))
        expected_root2 = GTreeNode(4)
        expected_root2.addChild(GTreeNode(3))
        expected_root2.addChild(GTreeNode(5))

        self.assertCrossoverResultsEqual(
            Crossovers.GTreeCrossoverSinglePointStrict,
            GTree(expected_root1),
            None,
            genome_attr_name=None,
            assertion_name='assetTreesEqual',
            crossover_extra_kwargs={'count': 1}
        )
        self.assertCrossoverResultsEqual(
            Crossovers.GTreeCrossoverSinglePointStrict,
            GTree(expected_root1),
            GTree(expected_root2),
            genome_attr_name=None,
            assertion_name='assetTreesEqual',
            crossover_extra_kwargs={'count': 2}
        )
