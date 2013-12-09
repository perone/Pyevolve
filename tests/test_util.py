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