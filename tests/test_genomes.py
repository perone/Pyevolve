import unittest

from mock import patch, MagicMock
from pyevolve.G2DCartesian import G2DCartesian, CartesianNode
import re
from random import choice, randint

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
            mock = MagicMock()
            inputs = []
            if key > 0:
                for i in xrange(0, randint(1, 3)):
                    inputs.append(choice(self.genome[0:key]))            
                
            mock.inputs = inputs
            self.genome[key] = mock
            self.genome[key].getPreviousNodes = MagicMock(return_value = inputs)
        paths = self.genome.getActiveNodes()
        self.assertTrue(len(paths) == 3)
        
    def test_genome_compiled_code(self):
        from math import sin
        expected_exprs = []
        values = [10, 50, 90]        
        def get_effect(arg):
            expected_exprs.append("sin(" + str(values.pop(0)) + ")")
            return expected_exprs[-1]
        
        for key, node in enumerate(self.genome):
            mock = MagicMock()
            mock.getExpression = MagicMock(side_effect = get_effect)  
            self.genome[key] = mock
                    
        compiled = self.genome.getCompiledCode()
        self.assertTrue(len(compiled) == self.outs)
        for comp, expr in zip(compiled, expected_exprs):
            self.assertEqual(eval(comp), eval(expr))
        
    def test_genome_to_graph(self):
        try:
            import pydot
        except ImportError:
            return        
        
        for key, node in enumerate(self.genome):
            mock = MagicMock()
            mock.params = {"p1" : 1}
            if key >= self.rows * self.cols + self.ins:
                mock.data = ""
            else:
                mock.data = str(key)
            inputs = []
            if key > 0:
                for i in xrange(0, randint(1, 3)):
                    inputs.append(choice(self.genome[0:key]))            
                
            mock.inputs = inputs
            self.genome[key] = mock
                
        graph = pydot.Dot(graph_type='graph')    
        self.genome.writeDotGraph(graph)
        self.assertTrue(len(graph.get_node_list()) >= self.genome.outputs)
                            
class CartesianNodeTestCase(unittest.TestCase):
    @patch('pyevolve.G2DCartesian.rand_randint')
    @patch('pyevolve.G2DCartesian.rand_uniform')
    def setUp(self, rand_uni, rand_int):
        rand_uni.return_value = 0.1313
        rand_int.return_value = 8
        CartesianNode.paramMapping = {"p1" : "rand_randint(0, 10)",
                                        "p2" : "rand_uniform(0,1)"}
        self.prev1 = CartesianNode(0, 1, {"a" : 1}, [])
        self.prev2 = CartesianNode(0, 2, {"b" : 1}, [])
        self.node = CartesianNode(1, 0, {"func3" : 3}, [self.prev1, self.prev2])
        self.outnode = CartesianNode(2, 0, {}, [self.node])
        
    def tearDown(self):
        self.node = None
        CartesianNode.paramMapping.clear()
        
    def test_node_init(self):
        self.assertFalse(self.node.data == None)
        self.assertTrue(len(self.node.params) == 
                        len(CartesianNode.paramMapping))
        
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
        CartesianNode.paramMapping = {"p1" : "rand_randint(0, 10)"}
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
                            
    def test_get_expression(self):    
        expected_expr = "func3( "
        expr = self.outnode.getExpression("")        
        match = re.search('func3\( [a-z], [a-z], \{"[a-z0-9]*" : (\d+\.)?\d+, '
                            '"[a-z0-9]*" : (\d+\.)?\d+\} \)', expr)     
        self.assertEqual(match.group(0), expr)
        
    