# 36-39, 47-48, 56, 60, 64-73, 77-79, 83-86, 90-92, 96-107, 125-127, 131, 135, 143, 147, 151, 155, 159, 163, 171,
# 175-178, 198-202, 206-207, 216-220, 223, 226-229, 232, 239, 246, 250-252, 256-262, 270, 274, 278, 282-289

# flake8: noqa
from collections import Iterable
from unittest import TestCase

from pyevolve import G1DBinaryString
from pyevolve import GAllele
from pyevolve import G1DList
from pyevolve import G2DBinaryString
from pyevolve import G2DList
from pyevolve.GenomeBase import G1DBase
from pyevolve.GenomeBase import GTreeBase
from pyevolve.GTree import GTree
from pyevolve.GTree import GTreeNode
from pyevolve.GTree import GTreeNodeBase
from pyevolve.GTree import GTreeNodeGP


class GAllelesTestCase(TestCase):

    def test_createAlleles_default(self):
        _alleles = GAllele.GAlleles(allele_list=None)
        self.assertTrue(hasattr(_alleles, 'allele_list'), True)
        self.assertTrue(hasattr(_alleles, 'homogeneous'), True)
        self.assertEqual(_alleles.allele_list, [])
        _alleles = GAllele.GAlleles(allele_list=[1,2,3])
        self.assertEqual(_alleles.allele_list, [1,2,3])
        _alleles = GAllele.GAlleles(homogeneous=True)
        self.assertEqual(_alleles.homogeneous, True)

    def test_Alleles_iadd(self):
        _alleles1 = GAllele.GAlleles(allele_list=[1, 2, 3])
        _alleles1 += 4
        self.assertEqual(_alleles1.allele_list, [1, 2, 3, 4])

    def test_Alleles_add(self):
        _alleles1 = GAllele.GAlleles(allele_list=[1, 2, 3])
        _alleles1.add(4)
        self.assertEqual(_alleles1.allele_list, [1, 2, 3, 4])
    
    def test_Alleles_slicing(self):
        # includes slice operation, getitem and setitem
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3])
        self.assertEqual(_alleles[1], 2)
        with self.assertRaises(Exception):
            _ = _alleles[4]
        _alleles[1] = 5
        self.assertEqual(_alleles[1], 5)
        self.assertEqual(_alleles[0:2], [1, 5])

    def test_Alleles_slicing_homogeneous(self):
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3], homogeneous=True)
        self.assertEqual(_alleles[2], 1)
        _alleles[1] = 5
        self.assertEqual(_alleles[0], 5)

    def test_Alleles_iter(self):
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3])
        self.assertIsInstance(iter(_alleles), Iterable)
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3], homogeneous=True)
        self.assertIsInstance(iter(_alleles), Iterable)

    def test_Alleles_len(self):
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3])
        self.assertEqual(len(_alleles), 3)
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3], homogeneous=True)
        self.assertEqual(len(_alleles), 1)

    def test_Alleles_repr(self):
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3])
        self.assertIsInstance(repr(_alleles), str)
        _alleles = GAllele.GAlleles(allele_list=[1, 2, 3], homogeneous=True)
        self.assertIsInstance(repr(_alleles), str)


class GAlleleListTestCase(TestCase):

    def test_createAlleleList_default(self):
        _allelelist = GAllele.GAlleleList()
        self.assertEqual(_allelelist.options, [])
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        self.assertEqual(_allelelist.options, [1, 2, 3])
    
    def test_AlleleList_clear(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        _allelelist.clear()
        self.assertEqual(_allelelist.options, [])
    
    def test_AlleleList_getRandomAllele(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        random_allele = _allelelist.getRandomAllele()
        self.assertIn(random_allele, _allelelist.options)

    def test_AlleleList_add(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        _allelelist.add(4)
        self.assertEqual(_allelelist.options, [1, 2, 3, 4])

    def test_AlleleList_slicing(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        self.assertEqual(_allelelist[0:2], [1, 2])
        self.assertEqual(_allelelist[1], 2)
        _allelelist[1] = 4
        self.assertEqual(_allelelist[1], 4)

    def test_AlleleList_iter(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        self.assertIsInstance(iter(_allelelist), Iterable)

    def test_AlleleList_len(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        self.assertEqual(len(_allelelist), 3)

    def test_AlleleList_remove(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        _allelelist.remove(2)
        self.assertEqual(_allelelist.options, [1, 3])

    def test_AlleleList_repr(self):
        _allelelist = GAllele.GAlleleList(options=[1, 2, 3])
        self.assertIsInstance(repr(_allelelist), str)


class GAlleleRangeTestCase(TestCase):

    def test_createAlleleRange(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        self.assertEqual(_allelerange.beginEnd, [(10, 20)])
        self.assertEqual(_allelerange.minimum, 10)
        self.assertEqual(_allelerange.maximum, 20)
        _allelerange = GAllele.GAlleleRange(1.0, 2.0, real=True)
        self.assertEqual(_allelerange.real, True)

    def test_AlleleRange_add(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        _allelerange.add(30, 40)
        self.assertEqual(_allelerange.beginEnd, [(10, 20), (30, 40)])
        self.assertEqual(_allelerange.minimum, 10)
        self.assertEqual(_allelerange.maximum, 40)
        with self.assertRaises(ValueError):
            _allelerange.add(40, 30)

    def test_AlleleRange_slicing(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        _allelerange.add(30, 40)
        self.assertEqual(_allelerange[0], (10, 20))
        _allelerange[1] = (50, 60)
        self.assertEqual(_allelerange[1], (50, 60))
        with self.assertRaises(ValueError):
            _allelerange[1] = (60, 50)

    def test_AlleleRange_iter(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        self.assertIsInstance(iter(_allelerange), Iterable)

    def test_AlleleRange_getMaximum(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        self.assertEqual(_allelerange.getMinimum(), 10)

    def test_AlleleRange_getMinimum(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        self.assertEqual(_allelerange.getMaximum(), 20)

    def test_AlleleRange_clear(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        _allelerange.clear()
        self.assertEqual(_allelerange.beginEnd, [])

    def test_AlleleRange_getRandomAllele(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        random_allele = _allelerange.getRandomAllele()
        self.assertTrue(random_allele,
                        any([x[0] <= random_allele <= x[1] for x in _allelerange.beginEnd]))
        _allelerange.add(30, 40)
        random_allele = _allelerange.getRandomAllele()
        self.assertTrue(random_allele,
                        any([x[0] <= random_allele <= x[1] for x in _allelerange.beginEnd]))
        _allelerange = GAllele.GAlleleRange(1.0, 2.0, real=True)
        random_allele = _allelerange.getRandomAllele()
        self.assertTrue(random_allele,
                        any([x[0] <= random_allele <= x[1] for x in _allelerange.beginEnd]))


    def test_AlleleRange_real(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        self.assertEqual(_allelerange.getReal(), False)
        _allelerange.setReal(flag=True)
        self.assertEqual(_allelerange.getReal(), True)

    def test_AlleleRange_len(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        _allelerange.add(30, 40)
        self.assertEqual(len(_allelerange), 2)

    def test_AlleleRange_repr(self):
        _allelerange = GAllele.GAlleleRange(10, 20)
        self.assertIsInstance(repr(_allelerange), str)