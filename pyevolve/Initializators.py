"""

:mod:`Initializators` -- initialization methods module
===================================================================

In this module we have the genetic operators of initialization for each
chromosome representation, the most part of initialization is done by
choosing random data.

.. note:: In Pyevolve, the Initializator defines the data type that will
          be used on the chromosome, for example, the :func:`G1DListInitializatorInteger`
          will initialize the G1DList with Integers.


"""

from random import randint as rand_randint, uniform as rand_uniform, choice as rand_choice, gauss as rand_gauss
import GTree
import G2DCartesian
import Util


#############################
##     1D Binary String    ##
#############################

def G1DBinaryStringInitializator(genome, **args):
    """ 1D Binary String initializator """
    genome.genomeList = [rand_choice((0, 1)) for _ in xrange(genome.getListSize())]


#############################
##     2D Binary String    ##
#############################

def G2DBinaryStringInitializator(genome, **args):
    """ Integer initialization function of 2D Binary String

    .. versionadded:: 0.6
       The *G2DBinaryStringInitializator* function
    """
    genome.clearString()

    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            random_gene = rand_choice((0, 1))
            genome.setItem(i, j, random_gene)


####################
##     1D List    ##
####################

def G1DListInitializatorAllele(genome, **args):
    """ Allele initialization function of G1DList

    To use this initializator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    """

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the G1DListInitializatorAllele, you must specify the 'allele' parameter")

    genome.genomeList = [allele[i].getRandomAllele() for i in xrange(genome.getListSize())]


def G1DListInitializatorInteger(genome, **args):
    """ Integer initialization function of G1DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    range_min = genome.getParam("rangemin", 0)
    range_max = genome.getParam("rangemax", 100)

    genome.genomeList = [rand_randint(range_min, range_max) for i in xrange(genome.getListSize())]


def G1DListInitializatorReal(genome, **args):
    """ Real initialization function of G1DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    range_min = genome.getParam("rangemin", 0)
    range_max = genome.getParam("rangemax", 100)

    genome.genomeList = [rand_uniform(range_min, range_max) for i in xrange(genome.getListSize())]


####################
##     2D List    ##
####################

def G2DListInitializatorInteger(genome, **args):
    """ Integer initialization function of G2DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    genome.clearList()

    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            randomInteger = rand_randint(genome.getParam("rangemin", 0),
                                         genome.getParam("rangemax", 100))
            genome.setItem(i, j, randomInteger)


def G2DListInitializatorReal(genome, **args):
    """ Integer initialization function of G2DList

    This initializator accepts the *rangemin* and *rangemax* genome parameters.

    """
    genome.clearList()

    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            randomReal = rand_uniform(genome.getParam("rangemin", 0),
                                      genome.getParam("rangemax", 100))
            genome.setItem(i, j, randomReal)


def G2DListInitializatorAllele(genome, **args):
    """ Allele initialization function of G2DList

    To use this initializator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    .. warning:: the :class:`GAllele.GAlleles` instance must have the homogeneous flag enabled

    """

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the G2DListInitializatorAllele, you must specify the 'allele' parameter")

    if not allele.homogeneous:
        Util.raiseException("to use the G2DListInitializatorAllele, the 'allele' must be homogeneous")

    genome.clearList()

    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            random_allele = allele[0].getRandomAllele()
            genome.setItem(i, j, random_allele)


####################
##      Tree      ##
####################

def GTreeInitializatorInteger(genome, **args):
    """ Integer initialization function of GTree

    This initializator accepts the *rangemin* and *rangemax* genome parameters.
    It accepts the following parameters too:

    *max_depth*
       The max depth of the tree

    *max_siblings*
       The number of maximum siblings of an node

    *method*
       The method, accepts "grow", "full" or "ramped".

    .. versionadded:: 0.6
       The *GTreeInitializatorInteger* function.
    """
    max_depth = genome.getParam("max_depth", 5)
    max_siblings = genome.getParam("max_siblings", 2)

    range_min = genome.getParam("rangemin", 0)
    range_max = genome.getParam("rangemax", 100)

    lambda_generator = lambda: rand_randint(range_min, range_max)

    method = genome.getParam("method", "grow")

    if method == "grow":
        root = GTree.buildGTreeGrow(0, lambda_generator, max_siblings, max_depth)
    elif method == "full":
        root = GTree.buildGTreeFull(0, lambda_generator, max_siblings, max_depth)
    elif method == "ramped":
        if Util.randomFlipCoin(0.5):
            root = GTree.buildGTreeGrow(0, lambda_generator, max_siblings, max_depth)
        else:
            root = GTree.buildGTreeFull(0, lambda_generator, max_siblings, max_depth)
    else:
        Util.raiseException("Unknown tree initialization method [%s] !" % method)

    genome.setRoot(root)
    genome.processNodes()
    assert genome.getHeight() <= max_depth


def GTreeInitializatorAllele(genome, **args):
    """ Allele initialization function of GTree

    To use this initializator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    .. warning:: the :class:`GAllele.GAlleles` instance **must** have the homogeneous flag enabled

    .. versionadded:: 0.6
       The *GTreeInitializatorAllele* function.
    """
    max_depth = genome.getParam("max_depth", 5)
    max_siblings = genome.getParam("max_siblings", 2)
    method = genome.getParam("method", "grow")

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the GTreeInitializatorAllele, you must specify the 'allele' parameter")

    if not allele.homogeneous:
        Util.raiseException("to use the GTreeInitializatorAllele, the 'allele' must be homogeneous")

    if method == "grow":
        root = GTree.buildGTreeGrow(0, allele[0].getRandomAllele, max_siblings, max_depth)
    elif method == "full":
        root = GTree.buildGTreeFull(0, allele[0].getRandomAllele, max_siblings, max_depth)
    elif method == "ramped":
        if Util.randomFlipCoin(0.5):
            root = GTree.buildGTreeGrow(0, allele[0].getRandomAllele, max_siblings, max_depth)
        else:
            root = GTree.buildGTreeFull(0, allele[0].getRandomAllele, max_siblings, max_depth)
    else:
        Util.raiseException("Unknown tree initialization method [%s] !" % method)

    genome.setRoot(root)
    genome.processNodes()
    assert genome.getHeight() <= max_depth


####################
##      Tree GP   ##
####################

def GTreeGPInitializator(genome, **args):
    """This initializator accepts the follow parameters:

    *max_depth*
       The max depth of the tree

    *method*
       The method, accepts "grow", "full" or "ramped"

    .. versionadded:: 0.6
       The *GTreeGPInitializator* function.
    """

    max_depth = genome.getParam("max_depth", 5)
    method = genome.getParam("method", "grow")
    ga_engine = args["ga_engine"]

    if method == "grow":
        root = GTree.buildGTreeGPGrow(ga_engine, 0, max_depth)
    elif method == "full":
        root = GTree.buildGTreeGPFull(ga_engine, 0, max_depth)
    elif method == "ramped":
        if Util.randomFlipCoin(0.5):
            root = GTree.buildGTreeGPFull(ga_engine, 0, max_depth)
        else:
            root = GTree.buildGTreeGPGrow(ga_engine, 0, max_depth)
    else:
        Util.raiseException("Unknown tree initialization method [%s] !" % method)

    genome.setRoot(root)
    genome.processNodes()
    assert genome.getHeight() <= max_depth
	
####################
##  Cartesian GP  ##
####################
	
def G2DCartesianInitializatorNode(genome, **args):
    """This initializator is for Cartesian Genetic Programming, it uses three 
        types of "slicers" from genome: inputs, internals and outputs. Every 
        input get single terminal from engine, internals get a set of possible
        functions, their parameters mapping set and previous available nodes 
        outputs get just previous available nodes. From ga_engine is uses:

    *gp_function_set*
        Dict of functions and their arguments counter founded automatically 
        after defining function prefix in ga_engine.

    *gp_terminals*
        List of terminals passed to ga_engine.
        
    *gp_args_mapping*
        Dict of parameters for node with value being a str generating value for 
        them via eval(), example: 
            {"param1" : "random.randint(0,10)"} 
        uses for parameter 'param1' random integer generator.

    .. versionadded::
       The *G2DCartesianInitializatorNode* function.
    """
    
    if not isinstance(genome, G2DCartesian.G2DCartesian):
        raise TypeError("Specified genome unsuitable for this Initializator.")
    
    ga_engine = args["ga_engine"]
    inputs = genome.inputs
    outputs = genome.outputs
    rows = genome.rows
    cols = genome.cols
    inputSlice = genome.inputSlice
    internalSlice = genome.internalSlice
    outputSlice = genome.outputSlice
    terminals = ga_engine.getParam("gp_terminals")
    functions_set = ga_engine.getParam("gp_function_set")
    args_mapping = ga_engine.getParam("gp_args_mapping")       

    if terminals is None:
        raise AssertionError("Empty terminal set.")
    if functions_set is None:
        raise AssertionError("Empty function set.")
    if args_mapping is None:
        raise AssertionError("Empty argument mapping set.")
    if not len(terminals) == inputs:
        raise AssertionError("Terminal set must be equal with input length.")

    G2DCartesian.CartesianNode.paramMapping = args_mapping
        
    nodes = []
    for counter, terminal in enumerate(terminals):
        nodes.append(G2DCartesian.CartesianNode(-1, counter, {terminal : 1}))
    genome[inputSlice] = nodes

    previous_nodes = genome[0:inputs]
    nodes = []
    for counter in xrange(0, rows * cols):
        nodes.append(G2DCartesian.CartesianNode(counter / cols, counter % cols, 
                    functions_set, previous_nodes))
        start = (counter / cols) * cols
        end = (start+cols)*((counter % cols) == (cols - 1))
        previous_nodes += nodes[start:end]
    genome[internalSlice] = nodes
	
    nodes = []    
    for counter in xrange(0, outputs):
        nodes.append(G2DCartesian.CartesianNode(rows, counter, {}, 
                    previous_nodes))
    genome[outputSlice] = nodes
