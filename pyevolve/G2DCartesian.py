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
   :func:`None`
   The Mutator for G2DCartesian
*Crossover*
   :func:`None`
   The Crossover for G2DCartesian
Class
-------------------------------------------------------------
"""

from GenomeBase import GenomeBase
import Consts
import random
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
                "inputSlice", "internalSlice", "outputSlice", "nodes"]

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
        g.nodes = copy.deepcopy(self.nodes)
        
    def getActiveNodes(self):
        """ Return list of lists with active paths in net, the size of list
        depends on the number of net outputs. It populates list in reverse
        direction, from output to input """
        actives = []
        for i in xrange(0, self.outputs):            
            actives.append([])
            self.nodes[-i-1].getPreviousNodes(actives[i])
        return actives
                
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
            self.data = random.choice(data_set.keys())
        except IndexError:
            self.data = ""

        try:
            inputs_count = data_set[self.data]-1
        except KeyError:
            inputs_count = 1

        if (len(previous_nodes) < inputs_count):
            raise ValueError("Bad data set and previous nodes values " 
                            "combination. If specified data set with input args"
                            " then previous nodes can not be empty!")
            
        for i in range(0, inputs_count):
            self.inputs.append(random.choice(previous_nodes))            
            
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
        
    def getPreviousNodes(self, nodes):
        """ Recursively returns previous, connected nodes in net of this node"""
        if len(self.inputs) == 0:
            return
        elif self.data is not "":
            nodes.append(self)

        for i in self.inputs:
            i.getPreviousNodes(nodes)

             
