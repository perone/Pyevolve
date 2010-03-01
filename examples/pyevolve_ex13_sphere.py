from pyevolve import G1DList, GSimpleGA, Selectors
from pyevolve import Initializators, Mutators, Consts, DBAdapters
import math

# This is the Sphere Function
def sphere(xlist):
   n = len(xlist)
   total = 0
   for i in range(n):
      total += (xlist[i]**2)
   return total

# Genome instance
genome = G1DList.G1DList(50)
genome.setParams(rangemin=-5.12, rangemax=5.13)
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

# The evaluator function (objective function)
genome.evaluator.set(sphere)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.minimax = Consts.minimaxType["minimize"]
ga.setGenerations(500)
ga.setMutationRate(0.02)

# Create DB Adapter and set as adapter
# sqlite_adapter = DBAdapters.DBSQLite(identify="sphere")
# ga.setDBAdapter(sqlite_adapter)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=20)

# Best individual
best = ga.bestIndividual()
print "\nBest individual score: %.2f" % (best.score,)
print best

