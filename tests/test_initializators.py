import unittest

from mock import MagicMock
from pyevolve.G1DBinaryString import G1DBinaryString
from pyevolve import Initializators
from pyevolve.G1DList import G1DList
from pyevolve.G2DList import G2DList
from pyevolve.GTree import GTree
from pyevolve.G2DCartesian import G2DCartesian
import random


class InitializatorsTestCase(unittest.TestCase):
    def test_binary_string_initializator(self):
        genome = G1DBinaryString(3)
        Initializators.G1DBinaryStringInitializator(genome)
        for gen in genome.genomeList:
            self.assertTrue(gen in [0, 1])

    def test_1d_list_real_initializator(self):
        genome = G1DList(3)
        Initializators.G1DListInitializatorReal(genome)
        for gen in genome.genomeList:
            self.assertTrue(type(gen) == float)

    def test_2d_list_integer_initializator(self):
        genome = G2DList(3, 3)
        Initializators.G2DListInitializatorInteger(genome)
        for gen_row in genome.genomeList:
            for gen in gen_row:
                self.assertTrue(type(gen) == int)

    def test_2d_list_real_initializator(self):
        genome = G2DList(3, 3)
        Initializators.G2DListInitializatorReal(genome)
        for gen_row in genome.genomeList:
            for gen in gen_row:
                self.assertTrue(type(gen) == float)

    def test_tree_integer_initializator(self):
        genome = GTree()
        genome.setParams(max_depth=3)
        Initializators.GTreeInitializatorInteger(genome)
        for gen in genome.getAllNodes():
            self.assertTrue(type(gen.getData()) == int)
            
class G2DCartesianInitializatorTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.engine = MagicMock();
        def getParams(value):
            if value == "gp_terminals":
                return ['a', 'b', 'c', 'd']
            elif value == "gp_function_set":
                return {"gp1" : 2, "gp2" : 2, "gp3" : 3}
            elif value == "gp_args_mapping":
                return {"arg1" : "random.randint(0,10)", 
                        "arg2" : "random.uniform(2.0,4.2)"}
                                
        self.engine.getParam = MagicMock(side_effect=getParams)
 
    def setUp(self):
        self.genome = G2DCartesian(2, 3, 4, 1)

    def tearDown(self):
        self.genome = None        
 
    def test_nodes_creation(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        for node in self.genome:
            self.assertFalse(node == None)

    def test_input_nodes_inputs(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        for node in self.genome[self.genome.inputSlice]:          
            self.assertTrue(len(node.inputs) == 0)
            
    def test_internal_nodes_inputs(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        for node in self.genome[self.genome.internalSlice]:          
            self.assertTrue(len(node.inputs) in xrange(1,3))
            for input in node.inputs:
                self.assertTrue(input.y < node.y)

    def test_output_nodes_inputs(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        for node in self.genome[self.genome.outputSlice]:          
            self.assertTrue(len(node.inputs) == 1)
            for input in node.inputs:
                self.assertTrue(input.y < node.y)
        
    def test_input_nodes_data_sets(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)       
        for node in self.genome[self.genome.inputSlice]:
            data = node.getData()
            self.assertTrue(data[0] in self.engine.getParam("gp_terminals"))
            
    def test_internal_nodes_data_sets(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)       
        for node in self.genome[self.genome.internalSlice]:
            data = node.getData()
            self.assertTrue(data[0] in self.engine.getParam("gp_function_set"))
            
            
    def test_output_nodes_data_sets(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)       
        for node in self.genome[self.genome.outputSlice]:
            data = node.getData()
            self.assertTrue(data[0] == "")
        
    def test_input_nodes_positions(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        for idx, node in enumerate(self.genome[self.genome.inputSlice]):
            self.assertTrue(node.x == idx)
            self.assertTrue(node.y == -1)
            
    def test_internal_nodes_positions(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        for idx, node in enumerate(self.genome[self.genome.internalSlice]):
            self.assertTrue(node.x == idx / self.genome.rows)
            self.assertTrue(node.y == idx % self.genome.cols)
            
    def test_output_nodes_positions(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        for idx, node in enumerate(self.genome[self.genome.outputSlice]):
            self.assertTrue(node.x == idx)
            self.assertTrue(node.y == self.genome.rows)

    def test_nodes_params(self):
        Initializators.G2DCartesianInitializatorNode(self.genome, 
                                                    ga_engine=self.engine)
        mapping = self.engine.getParam("gp_args_mapping")
        for node in self.genome:      
            for key in mapping.keys():            
                self.assertTrue(key in node.params)
                self.assertTrue(type(eval(mapping[key])) == 
                                type(node.params[key]))

    def test_empty_functions(self):
        eng = MagicMock()
        def getParams(value):
            if value == "gp_terminals":
                return ['a', 'b', 'c', 'd']
            return None
                
        eng.getParam = MagicMock(side_effect=getParams)
        self.assertRaises(AssertionError, 
                            Initializators.G2DCartesianInitializatorNode, 
                            self.genome, ga_engine=eng)
            
    def test_empty_terminals(self):
        eng = MagicMock()
        def getParams(value):
            if value == "gp_function_set":
                return {"gp1" : 2, "gp2" : 2, "gp3" : 3}
            return None
                
        eng.getParam = MagicMock(side_effect=getParams)        
        self.assertRaises(AssertionError, 
                            Initializators.G2DCartesianInitializatorNode, 
                            self.genome, ga_engine=eng)
        
    def test_empty_mapping(self):
        eng = MagicMock()
        def getParams(value):
            if value == "gp_terminals":
                return ['a', 'b', 'c', 'd']
            elif value == "gp_function_set":
                return {"gp1" : 2, "gp2" : 2, "gp3" : 3}
            return None
                
        eng.getParam = MagicMock(side_effect=getParams)        
        self.assertRaises(AssertionError, 
                            Initializators.G2DCartesianInitializatorNode, 
                            self.genome, ga_engine=eng)
        
    def test_empty_engine(self):
        self.assertRaises(KeyError, 
                            Initializators.G2DCartesianInitializatorNode, 
                            self.genome)
        
    def test_mismatch_input_with_terminals(self):
        eng = MagicMock()
        def getParams(value):
            if value == "gp_terminals":
                return ['a', 'b', 'c']
            if value == "gp_function_set":
                return {"gp1" : 2, "gp2" : 2, "gp3" : 3}
                
        eng.getParam = MagicMock(side_effect=getParams)
        self.assertRaises(AssertionError, 
                            Initializators.G2DCartesianInitializatorNode, 
                            self.genome, ga_engine=eng)
        
    def test_bad_genome(self):
        genome = G1DList()
        self.assertRaises(TypeError, 
                            Initializators.G2DCartesianInitializatorNode, 
                            genome)
        
