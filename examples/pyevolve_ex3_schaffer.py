from pyevolve import G1DList, GSimpleGA, Selectors
from pyevolve import Initializators, Mutators, Consts
import math

# This is the Schaffer F6 Function
# This function has been conceived by Schaffer, it's a 
# multimodal function and it's hard for GAs due to the
# large number of local minima, the global minimum is
# at x=0,y=0 and there are many local minima around it
def schafferF6(genome):
   t1 = math.sin(math.sqrt(genome[0]**2 + genome[1]**2));
   t2 = 1.0 + 0.001*(genome[0]**2 + genome[1]**2);
   score = 0.5 + (t1*t1 - 0.5)/(t2*t2)
   return score

def run_main():
   # Genome instance
   genome = G1DList.G1DList(2)
   genome.setParams(rangemin=-100.0, rangemax=100.0, bestrawscore=0.0000, rounddecimal=4)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

   # The evaluator function (objective function)
   genome.evaluator.set(schafferF6)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.selector.set(Selectors.GRouletteWheel)

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(8000)
   ga.setMutationRate(0.05)
   ga.setPopulationSize(100)
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=250)

   # Best individual
   best = ga.bestIndividual()
   print best
   print "Best individual score: %.2f" % best.getRawScore()

if __name__ == "__main__":
   run_main()
