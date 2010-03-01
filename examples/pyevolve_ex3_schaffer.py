# $Id: pyevolve_ex3_schaffer.py 150 2009-01-18 19:29:13Z christian.perone $
from pyevolve import G1DList, GSimpleGA, Selectors
from pyevolve import Initializators, Mutators, Consts
import math

# This is the Schaffer F6 Function, a deceptive function
def schafferF6(xlist):
   t1 = math.sin(math.sqrt(xlist[0]*xlist[0] + xlist[1]*xlist[1]));
   t2 = 1 + 0.001*(xlist[0]*xlist[0] + xlist[1]*xlist[1]);
   score = 0.5 + (t1*t1 - 0.5)/(t2*t2)
   return score

# Genome instance
genome = G1DList.G1DList(2)
genome.setParams(rangemin=-100, rangemax=100, bestRawScore=0.00, roundDecimal=2)
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

# The evaluator function (objective function)
genome.evaluator.set(schafferF6)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)

ga.minimax = Consts.minimaxType["minimize"]
ga.setGenerations(5000)
ga.setMutationRate(0.05)
ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=100)

# Best individual
best = ga.bestIndividual()
print "\nBest individual score: %.2f" % (best.score,)
print best
