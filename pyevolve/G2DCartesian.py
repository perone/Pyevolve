"""
:mod:`G2DCartesian` -- the 2D cartesian net chromosome
================================================================
This is the 2D Cartesian Net representation for Cartesian Genetic Programming
(CGP), this net consist of nodes which hold function or terminals (like in 
Genetic Programming).
This chromosome class extends the :class:`GenomeBase.GenomeBase`.
Default Parameters
-------------------------------------------------------------
*Initializator*
   :func:`Initializators.G2DCartesianInitializatorNode`
   The Node Initializator for G2DCartesian
*Mutator*
   :func:`Mutators.G2DCartesianMutatorNodeInputs`
   :func:`Mutators.G2DCartesianMutatorNodeParams`
   :func:`Mutators.G2DCartesianMutatorNodeFunction`
   :func:`Mutators.G2DCartesianMutatorNodesOrder`
   The Mutators for G2DCartesian
*Crossover*
   :func:`Crossovers.G2DCartesianCrossoverNode`
   The Crossover for G2DCartesian
Class
-------------------------------------------------------------
"""

from GenomeBase import GenomeBase
import Consts
from random import randint as rand_randint, choice as rand_choice
from random import uniform as rand_uniform, gauss as rand_gauss
import pydot
import copy

class G2DCartesian(GenomeBase):

    """ G2DCartesian Class - The 2D Cartesian Net chromosome representation
     Inheritance diagram for :class:`G2DCartesian.G2DCartesian`:
    .. inheritance-diagram:: G2DCartesian.G2DCartesian
    **Examples**
       The instantiation
          >>> genome1 = G2DCartesian.G2DCartesian(2, 3, 4, 2)
       Compare
          >>> genome2 = genome1.clone()
          >>> genome2 == genome1
          True
       Size, slice, get/set, append
          >>> len(genome)
          12
          >>> genome
          (...)
          [None, None, None, None, None, None, None, None, None, None, None, 
          None]
          >>> genome[1] = 2
          >>> genome
          (...)
          [None, 2, None, None, None, None, None, None, None, None, None, None]
          >>> genome[1]
          2
    :param rows: the number of rows in the net
    :param cols: the number of columns in the net
    :param inputs: the number of inputs nodes
    :param outputs: the number of output nodes
    """
	
    __slots__ = ["inputs", "outputs", "cols", "rows", "internalNodes", 
                "inputSlice", "internalSlice", "outputSlice", "nodes",
                "reevaluate", "expressionNodes"]

    def __init__(self, rows, cols, inputs, outputs, cloning = False):
        """ The initializator of G2DCartesian representation,
        rows, cols, inputs and outputs must be specified and none of them can
        equal to 0"""
        if (rows * cols * inputs * outputs) == 0:
            raise ValueError("One of the genome parameter equals 0.")
    
        super(G2DCartesian, self).__init__()
        self.rows = rows
        self.cols = cols
        self.inputs = inputs
        self.outputs = outputs
        self.internalNodes = rows*cols
        self.nodes = [None]*(rows*cols+outputs+inputs)				
        self.inputSlice = slice(0,self.inputs)
        self.internalSlice = slice(self.inputs, self.inputs+self.internalNodes)
        self.outputSlice = slice(self.inputs+self.internalNodes, 
                                self.inputs+self.internalNodes+self.outputs)
        self.expressionNodes = {}
        self.reevaluate = True

        if not cloning:
            self.initializator.set(Consts.CDefG2DCartesianInit)
            self.mutator.set(Consts.CDefG2DCartesianMutator)
            self.crossover.set(Consts.CDefG2DCartesianCrossover)

    def __eq__(self, other):
        """ Compares one chromosome with another """
        cond1 = (self.nodes == other.nodes)
        cond2 = (self.rows == other.rows)
        cond3 = (self.cols == other.cols)
        return True if cond1 and cond2 and cond3 else False
        
    def __getitem__(self, key):
        """ Return the specified node of net (including inputs and outputs)"""
        return self.nodes[key]
        
    def __iter__(self):
        """ Iterator support to the nodes """
        return iter(self.nodes)   

    def __len__(self):
        """ Return the number of all nodes in net """
        return len(self.nodes)

    def __repr__(self):
        """ Return a string representation of Genome """
        ret = GenomeBase.__repr__(self)
        ret += "- G2DCartesian\n"
        ret += "\tList size:\t %s\n" % (len(self.nodes,))
        ret += "\tList:\t\t %s\n\n" % (self.nodes,)
        return ret

    def __setitem__(self, key, value):
        """ Set the specified node in net """
        self.nodes[key] = value        
       
    def clone(self):
        """ Return a new instace copy of the genome

        :rtype: the G2DCartesian clone instance

        """
        newcopy = G2DCartesian(self.rows, self.cols, self.inputs, self.outputs, 
                              True)
        self.copy(newcopy)
        return newcopy

    def copy(self, g):
        """ Copy genome to 'g'

        Example:
           >>> genome_origin.copy(genome_destination)

        :param g: the destination G2DCartesian instance

        """
        GenomeBase.copy(self, g)
        g.expressionNodes = self.expressionNodes.copy()
        g.reevaluate = self.reevaluate
        g.nodes = copy.deepcopy(self.nodes)
        
    def evaluate(self, **args):
        """ Overloaded method of GenomeBase. It is performance improvement,
        genome score is evaluated only when mutations had influence on nodes
        active in the expression path """
        if self.reevaluate:
            super(G2DCartesian, self).evaluate(**args)
            self.expressionNodes.clear()
            for idx, path in enumerate(self.getActiveNodes()):
                for node in path:
                    self.expressionNodes[(node.x, node.y)] = True
                out = self.nodes[-idx-1]
                self.expressionNodes[(out.x, out.y)] = True
        
    def getActiveNodes(self):
        """ Return list of lists with active paths in net, the size of list
        depends on the number of net outputs. It populates list in reverse
        direction, from output to input """
        actives = []
        for i in xrange(0, self.outputs):            
            actives.append([])
            self.nodes[-i-1].getPreviousNodes(actives[i])
        return actives
        
    def getCompiledCode(self):
        """ Returns list of expressions from the genome, size of list depends on
        outputs count. Expressions are already a python compile object """
        expr = [None] * self.outputs
        for i in xrange(0, self.outputs):
            expr[i] = self.nodes[-i-1].getExpression("")
        compiled = []
        for e in expr:
            compiled.append(compile(e, "<string>", "eval"))
        return compiled

    def mutate(self, **args):
        """ Overloaded method of GenomeBase. Mutators of G2DCartesian return
        list of mutated nodes and if any of them is on the list of active
        expression nodes then genome flag to reevaluate is set """
        self.reevaluate = False
        mutated_nodes = []
        for it in self.mutator.applyFunctions(self, **args):
            mutated_nodes += it

        for node in mutated_nodes:
            if self.expressionNodes.has_key((node.x, node.y)):
                self.reevaluate = True
                return len(mutated_nodes)
        
        return len(mutated_nodes)                    
        
    def writeDotGraph(self, graph):
        """ Populates graph for pydot from active expression of genome """
        node_counter = 0
        for out in xrange(0, self.outputs):            
            node_stack = []
            node_dict = {}
            node_stack.append(self.nodes[-1-out])
            while node_stack:
                current_node = node_stack.pop()
                if current_node.data != "":
                    node_label = current_node.data
                    for param in current_node.params.keys():
                        node_label += " " + str(current_node.params[param])
                    graph.add_node(pydot.Node(str(node_counter), 
                                    label = node_label))
                    if current_node in node_dict:
                        graph.add_edge(pydot.Edge(node_dict[current_node], 
                                                    str(node_counter)))

                for input in current_node.inputs:                
                    node_stack.append(input)
                    if current_node.data != "":
                        node_dict[input] = str(node_counter)
                if current_node.data != "":
                    node_counter += 1
                
class CartesianNode():

    """ CartesianNode Class - The Cartesian Node representation
    **Examples**
       The instantiation
          >>> node = G2DCartesian.CartesianNode(1, 0, 
                                        {"func3" : 3}, [self.prev1, self.prev2])

       Very important thing for future developer is passing correct values for 
       data_set and previous_nodes. They are slightly different for input, 
       internal and output nodes in Cartesian Genetic Programming.
       
       Input node:
          >>> node = G2DCartesian.CartesianNode(1, 1, {"b" : 1}, [])
       No previous nodes and every function in data_set must have not more than
       one argument (for 'args', in fact it is zero arguments).
       Internal node:
          >>> node = G2DCartesian.CartesianNode(1, 1, {"f1" : 3}, 
                                                [self.prev1, self.prev2])
       It should have previous_nodes (at least input nodes!) and there are no
       constraints on functions dictionary and their inputs.
       Output node:
          >>> node = G2DCartesian.CartesianNode(1, 1, {}, 
                                                [self.prev1, self.prev2])
       No functions passed to output nodes, they just map net to the world. In
       previous nodes they should have all existing nodes except those being
       outputs.
       
    :param position_x: row position in the net
    :param position_y: column position in the net
    :param data_set: dictionary of functions which can be assigned to this node 
                     and number of their args
    :param previous_nodes: list of nodes which can be connected as inputs to
                           this node
    """

    paramMapping = {}

    def __init__(self, position_x, position_y, data_set = {}, 
                previous_nodes = []):
        """ The initializator of CartesianNode representation,
        position_x and position_y must be specified, data_set and previous_nodes
        depends on type of the node """
        self.data = None
        self.inputs = []
        self.params = {}
        self.x = position_x
        self.y = position_y

        try:
            self.data = rand_choice(data_set.keys())
        except IndexError:
            self.data = ""

        try:
            inputs_count = data_set[self.data]-1
        except KeyError:
            inputs_count = 1

        if (len(previous_nodes) == 0 and inputs_count > 0):
            raise ValueError("Bad data set and previous nodes values " 
                            "combination. If specified data set with input args"
                            " then previous nodes can not be empty!")
            
        for i in range(0, inputs_count):
            self.inputs.append(rand_choice(previous_nodes))            
            
        for param in CartesianNode.paramMapping.keys():
            self.params[param] = eval(CartesianNode.paramMapping[param])
            
    def __repr__(self):
        """ Return a string representation of Genome """
        ret = "\n\tCartesianNode [%s, %s] - " % (self.x, self.y)
        ret += "Data: %s" % (self.data)
        for i in self.inputs:
            ret += " Input: [%s, %s]" % (i.x, i.y)
        return ret

    def getData(self):
        """ Return tuple with node value and number of its input args """
        return (self.data, len(self.inputs))
        
    def getExpression(self, expr):
        """ Recursively iterates through input nodes of current node and return
        merged expression (function in the node and params) in string format """
        if self.data is not "":
            expr += self.data
            if self.inputs:
                expr += "( "
                input_counter = 0
                for idx, input in enumerate(self.inputs):
                    expr += input.getExpression("")                    
                    if idx < len(self.inputs)-1:
                        expr += ", "
                        
                expr += ", {"                
                for idx, param in enumerate(self.params.keys()):
                    expr += "\"" + param + "\"" + " : "
                    expr += str(self.params[param])
                    if idx < len(self.params)-1:
                        expr += ", "              
                expr += "} )"
        else:
            expr += self.inputs[0].getExpression("")
        return expr
        
    def getPreviousNodes(self, nodes):
        """ Recursively returns previous, connected nodes in net of this node"""
        if len(self.inputs) == 0:
            return
        elif self.data is not "":
            nodes.append(self)

        for i in self.inputs:
            i.getPreviousNodes(nodes)

             
