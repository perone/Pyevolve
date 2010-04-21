from pyevolve import G1DList, GSimpleGA, Selectors
from pyevolve import Initializators, Mutators, Consts, DBAdapters
import math

# This is the Rastringin Function, a deception function
def ackley(xlist):
   sum1 = 0
   score = 0
   n = len(xlist)
   for i in xrange(n):
      sum1 += xlist[i]*xlist[i]
   t1 = math.exp(-0.2*(math.sqrt((1.0/5.0)*sum1)))

   sum1 = 0
   for i in xrange(n):
      sum1 += math.cos(2.0*math.pi*xlist[i]);
   t2 = math.exp((1.0/5.0)*sum1);
   score = 20 + math.exp(1) - 20 * t1 - t2;

   return score


def run_main():
   # Genome instance
   genome = G1DList.G1DList(5)
   genome.setParams(rangemin=-8, rangemax=8,  bestrawscore=0.00, rounddecimal=2)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

   # The evaluator function (objective function)
   genome.evaluator.set(ackley)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(1000)
   ga.setMutationRate(0.04)
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

   # Create DB Adapter and set as adapter
   # sqlite_adapter = DBAdapters.DBSQLite(identify="ackley")
   # ga.setDBAdapter(sqlite_adapter)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=50)

   # Best individual
   best = ga.bestIndividual()
   print "\nBest individual score: %.2f" % (best.getRawScore(),)
   print best

if __name__ == "__main__":
   run_main()
