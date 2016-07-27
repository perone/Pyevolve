from unittest import TestCase

from pyevolve import Util


class UtilTestCase(TestCase):
    def test_listSwapElement(self):
        _list = [1, 2, 3]
        Util.listSwapElement(_list, 0, 1)
        self.assertEqual(_list, [2, 1, 3])

    def test_randomFlipCoin_border_cases(self):
        self.assertEqual(Util.randomFlipCoin(0.0), False)
        self.assertEqual(Util.randomFlipCoin(1.0), True)

    def test_list2DSwapElement(self):
        _list = [[1, 2, 3], [4, 5, 6]]
        Util.list2DSwapElement(_list, (0, 1), (1, 1))
        self.assertEqual(_list, [[1, 5, 3], [4, 2, 6]])
        
try:
    import numpy as np
    
    class VectorErrorAccumulatorTestCase(TestCase):
        def setUp(self):
            np.empty([2, 2])
            self.VEC = Util.VectorErrorAccumulator(False, False)
            self.VECC = Util.VectorErrorAccumulator(True, False)
            self.VECZ = Util.VectorErrorAccumulator(False, True)
            self.VECCZ = Util.VectorErrorAccumulator(True, True)
            self.target = np.ones([12, 12])
            self.evaluated = np.zeros([12, 12])
    
        def test_init_standard(self):
            self.assertTrue(self.VEC.non_zeros == 0)
            self.assertTrue((self.VEC.confusion == np.zeros([2, 2])).all())
            
        def test_init_without_any(self):
            self.assertTrue(self.VEC.calculate_confusion == False)
            self.assertTrue(self.VEC.calculate_non_zeros == False)
            
        def test_init_with_confusion(self):
            self.assertTrue(self.VECC.calculate_confusion == True)
            self.assertTrue(self.VECC.calculate_non_zeros == False)
            
        def test_init_with_confusion_and_zeros(self):
            self.assertTrue(self.VECCZ.calculate_confusion == True)
            self.assertTrue(self.VECCZ.calculate_non_zeros == True)
            
        def test_init_with_zeros(self):
            self.assertTrue(self.VECZ.calculate_confusion == False)
            self.assertTrue(self.VECZ.calculate_non_zeros == True)
            
            
        def test_reset_empty(self):
            self.VEC.reset()
            self.assertTrue(self.VEC.non_zeros == 0)
            self.assertTrue((self.VEC.confusion == np.zeros([2, 2])).all())
            
        def test_reset_non_empty(self):
            self.VEC.non_zeros = 10
            self.VEC.confusion = np.ones([2 ,2])
            self.VEC.reset()
            self.assertTrue(self.VEC.non_zeros == 0)
            print self.VEC.confusion
            self.assertTrue((self.VEC.confusion == np.zeros([2, 2])).all())
            
        def test_append_to_empty(self):
            self.VEC.append(self.target, self.evaluated)
            self.assertTrue(self.VEC.acc_len == 144)
            
        def test_append_to_non_empty(self):
            self.VEC.append(self.target, self.evaluated)
            self.VEC.append(self.target, self.evaluated)
            self.assertTrue(self.VEC.acc_len == 144*2)
            
        def test_get_confusion_matrix(self):
            self.VECC.append(self.target, self.evaluated)
            ret = self.VECC.getConfusionMatrix()
            self.assertTrue((np.array([[144, 0], [0, 0]]) == ret).all())            
            
        def test_get_zeros(self):
            self.VECZ.append(self.target, self.evaluated)
            ret = self.VECZ.getZeros()
            self.assertTrue(ret == 0)
            
        def test_get_non_zeros(self):
            self.VECCZ.append(self.target, self.evaluated)
            ret = self.VECCZ.getNonZeros()            
            self.assertTrue(ret == 144)
            
except:
    pass