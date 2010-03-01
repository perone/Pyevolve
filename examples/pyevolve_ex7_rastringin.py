from pyevolve import G1DList, GSimpleGA
from pyevolve import Initializators, Mutators, Consts
import math

# This is the Rastringin Function, a deception function
def rastringin(xlist):
   n = len(xlist)
   total = 0
   for i in range(n):
      total += xlist[i]**2 - 10*math.cos(2*math.pi*xlist[i])
   return (10*n) + total

# Genome instance
genome = G1DList.G1DList(20)
genome.setParams(rangemin=-5.2, rangemax=5.30)
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

# The evaluator function (objective function)
genome.evaluator.set(rastringin)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.minimax = Consts.minimaxType["minimize"]
ga.setGenerations(800)
ga.setMutationRate(0.05)

# Create DB Adapter and set as adapter
#sqlite_adapter = DBAdapters.DBSQLite(identify="rastringin")
#ga.setDBAdapter(sqlite_adapter)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=50)

# Best individual
best = ga.bestIndividual()
print "\nBest individual score: %.2f" % (best.getRawScore(),)
print best

