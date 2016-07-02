import unittest

from mock import MagicMock
from pyevolve.G2DCartesian import G2DCartesian, CartesianNode

class G2DCartesianGenomeTestCase(unittest.TestCase):
    def setUp(self):
        self.rows = 4
        self.cols = 5
        self.ins = 1
        self.outs = 3
        self.genome = G2DCartesian(self.rows, self.cols, self.ins, self.outs)
        
    def tearDown(self):
        self.genome = None
        
    def test_genome_init(self):        
        self.assertTrue(self.genome.rows == self.rows)
        self.assertTrue(self.genome.cols == self.cols)
        self.assertTrue(self.genome.inputs == self.ins)
        self.assertTrue(self.genome.outputs == self.outs)
        self.assertTrue(self.genome.internalNodes == self.rows * self.cols)
        self.assertTrue(self.genome.inputSlice == slice(0,self.ins))
        self.assertTrue(self.genome.internalSlice == slice(self.ins, self.ins + 
                                                       (self.rows * self.cols)))
        self.assertTrue(self.genome.outputSlice == slice(self.ins +
                                                        (self.rows * self.cols), 
                                                        self.ins + 
                                                        (self.rows * self.cols) 
                                                        + self.outs))
                                                        
    def test_genome_clone(self):
        genomeClone = self.genome.clone()
        self.assertTrue(genomeClone == self.genome)
        
    def test_genome_nodes(self):
        self.assertTrue(len(self.genome) == self.rows * self.cols + self.ins + 
                                    self.outs)
        self.assertTrue(self.genome[0] == None)
        self.assertTrue(self.genome[self.rows * self.cols + self.ins + 
                                    self.outs - 1] == None)
        self.assertRaises(IndexError, self.genome.__getitem__, 
                            self.rows*self.cols*self.cols)
                            
    def test_genome_zero_param(self):
        self.assertRaises(ValueError, G2DCartesian, 0, 1, 2, 10)

    def test_genome_active_nodes(self):
        for key, node in enumerate(self.genome):
            self.genome[key] = MagicMock()
            self.genome[key].getPreviousNodes = MagicMock(return_value = [])
        paths = self.genome.getActiveNodes()
        self.assertTrue(len(paths) == 3)
                            
class CartesianNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.prev1 = CartesianNode(0, 1, {"a" : 1}, [])
        self.prev2 = CartesianNode(0, 2, {"b" : 1}, [])
        self.node = CartesianNode(1, 0, {"func3" : 3}, [self.prev1, self.prev2])
        
    def tearDown(self):
        self.node = None
        CartesianNode.paramMapping.clear()
        
    def test_node_init(self):
        self.assertFalse(self.node.data == None)
        self.assertTrue(len(self.node.params) == 0)
        
    def test_node_init_input_like(self):
        node = CartesianNode(1, 1, {"b" : 1}, [])
        data = node.getData()
        self.assertTrue(data[0] == "b")
        self.assertTrue(data[1] == 0)
        
    def test_node_init_internal_like(self):
        node = CartesianNode(1, 1, {"f1" : 3}, [self.prev1, self.prev2])
        data = node.getData()
        self.assertTrue(data[0] == "f1")
        self.assertTrue(data[1] == 2)
        
    def test_node_init_output_like(self):
        node = CartesianNode(1, 1, {}, [self.prev1, self.prev2])
        data = node.getData()
        self.assertTrue(data[0] == "")
        self.assertTrue(data[1] == 1)
        
    def test_node_init_empty_previous_with_bad_function_set(self):
        self.assertRaises(ValueError, CartesianNode, 0, 0, {"f2" : 3})
        
    def test_node_param_mapping(self):
        CartesianNode.paramMapping = {"p1" : "random.randint(0, 10)"}
        node = CartesianNode(1, 1, {"f1" : 3}, [self.prev1, self.prev2])
        self.assertTrue(len(node.params) == len(CartesianNode.paramMapping))
        
    def test_node_previous_for_input(self):
        node = CartesianNode(1, 1, {"b" : 1}, [])
        previous = []
        node.getPreviousNodes(previous)
        self.assertTrue(len(previous) == 0)
        
    def test_node_previous_for_internal(self):
        previous = []
        self.node.getPreviousNodes(previous)
        self.assertTrue(len(previous) > 0)
        
    def test_node_previous_for_output(self):
        prev = CartesianNode(1, 1, {"f" : 2}, [self.prev1, self.prev2])
        node = CartesianNode(1, 1, {}, [prev])
        previous = []
        node.getPreviousNodes(previous)
        self.assertTrue(len(previous) > 0)
        
    