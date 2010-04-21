from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors

# The step callback function, this function
# will be called every step (generation) of the GA evolution
def evolve_callback(ga_engine):
   generation = ga_engine.getCurrentGeneration()
   if generation % 100 == 0:
      print "Current generation: %d" % (generation,)
      print ga_engine.getStatistics()
   return False

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(genome):
   score = 0.0
   # iterate over the chromosome
   for value in genome:
      if value==0: score += 0.1
   return score

def run_main():
   # Genome instance
   genome = G1DList.G1DList(200)
   genome.setParams(rangemin=0, rangemax=10)

   # The evaluator function (objective function)
   genome.evaluator.set(eval_func)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(800)
   ga.stepCallback.set(evolve_callback)

   # Do the evolution
   ga.evolve()

   # Best individual
   print ga.bestIndividual()

if __name__ == "__main__":
   run_main()

