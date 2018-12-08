from unittest import TestCase

from builtins import int

from pyevolve import Statistics


class StatisticsTestCase(TestCase):

    def setUp(self):
        self._stats = Statistics.Statistics()

    def test_lenStatistics(self):
        self.assertEqual(len(self._stats), self._stats.internalDict.__len__())

    def test_reprStatistics(self):
        # it should be just successfully generated string
        self.assertIsInstance(repr(self._stats), str)

    def test_statisticsAsTuple(self):
        # modify to have some probable type diversity
        self._stats["rawMax"] = 9223372036854775808  # it will be long on Py 2
        self._stats["rawMin"] = 1.2  # float
        stat_tuple = self._stats.asTuple()
        self.assertIsInstance(stat_tuple, tuple)
        self.assertEqual(len(stat_tuple), len(self._stats))
        self.assertTrue(all(isinstance(x, (int, float)) for x in stat_tuple))

    def test_clearStatistics(self):
        len_before_clear = len(self._stats)
        self._stats.clear()
        len_after_clear = len(self._stats)
        self.assertEqual(len_before_clear, len_after_clear)
        clean_stats = Statistics.Statistics()
        self.assertEqual(self._stats.internalDict, clean_stats.internalDict)

    def test_statisticsItems(self):
        stat_items = self._stats.items()
        stat_names = list(self._stats.internalDict.keys())
        self.assertIsInstance(stat_items, list)
        self.assertEqual(len(stat_items), len(self._stats))
        self.assertTrue(all(isinstance(x[1], (int, float)) for x in stat_items))
        self.assertTrue(set(stat_names), set([x[0] for x in stat_items]))

    def test_cloneStatistics(self):
        clone = self._stats.clone()
        self.assertIsNot(clone, self._stats)
        self.assertEqual(clone.internalDict, self._stats.internalDict)
        self.assertEqual(clone.descriptions, self._stats.descriptions)

    def test_copyStatistics(self):
        target = Statistics.Statistics()
        self._stats.copy(target)
        self.assertEqual(self._stats.internalDict, target.internalDict)
        self.assertEqual(self._stats.descriptions, target.descriptions)
        self.assertIsNot(self._stats.internalDict, target.internalDict)
        self.assertIsNot(self._stats.descriptions, target.descriptions)
